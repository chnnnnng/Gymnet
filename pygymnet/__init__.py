"""
Veins-Gym base structures to create gym environments from veins simulations.
"""

import atexit
import logging
import os
import signal
import subprocess
import sys
from typing import Any, Dict, NamedTuple
import numpy as np
import zmq
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from . import veinsgym_pb2
from .config import gymnet_config

SENTINEL_EMPTY_SPACE = gym.spaces.Space()
SENTINEL_NO_SEED_GIVEN = None

# register veins_gym as a gym environment
gym.register(
    id="gymnet-v1",
    entry_point="pygymnet:VeinsEnv",
    kwargs=gymnet_config
)


class StepResult(NamedTuple):
    """Result record from one step in the invironment."""

    observation: Any
    reward: np.float32
    done: bool
    truncated: bool
    info: Dict


def ensure_valid_scenario_dir(scenario_dir):
    """
    Raise an exception if path is not a valid scenario directory.
    """
    if scenario_dir is None:
        raise ValueError("No scenario_dir given.")
    if not os.path.isdir(scenario_dir):
        raise ValueError(f"The scenario_dir {scenario_dir} does not point to a directory.")
    if not os.path.exists(os.path.join(scenario_dir, "omnetpp.ini")):
        raise FileNotFoundError(f"The scenario_dir {scenario_dir} needs to contain an omnetpp.ini file.")
    return True


def launch_veins(
    scenario_dir,
    executable_path,
    env_path,
    seed,
    port,
    print_stdout=False,
    extra_args=None,
    user_interface="Cmdenv",
    sim_time_limit="1s",
    config="General",
):
    """
    Launch a veins experiment and return the process instance.

    All extra_args keys need to contain their own -- prefix.
    The respective values need to be correctly quouted.
    """
    command = [
        executable_path,
        f"-u{user_interface}",
        f"-c{config}",
        f"--sim-time-limit={sim_time_limit}",
        f"--seed-set={seed}",
        f"--*.manager.seed={seed}",
        f"--*.gym_connection.port={port}",
    ]
    
    env = os.environ.copy()
    if env_path:
        env["PATH"] = env_path + env["PATH"]

    extra_args = dict() if extra_args is None else extra_args
    for key, value in extra_args.items():
        command.append(f"{key}={value}")
    logging.debug(f"Launching veins experiment using command {command} in directory {scenario_dir} with env:path={env_path}")
    stdout = sys.stdout if print_stdout else subprocess.DEVNULL
    process = subprocess.Popen(command, stdout=stdout, stderr=stdout, cwd=scenario_dir, env=env)
    logging.debug("Veins process launched with pid %d", process.pid)
    return process


def shutdown_veins(process, gracetime_s=1.0):
    """
    Shut down veins if it still runs.
    """
    
    logging.debug("Try shutdown Veins process %d", process.pid)
    
    process.poll()
    if process.poll() is not None:
        logging.debug(
            "Veins process %d was shut down already with returncode %d.",
            process.pid,
            process.returncode,
        )
        return
    process.terminate()
    try:
        process.wait(gracetime_s)
    except subprocess.TimeoutExpired as _exc:
        logging.warning(
            "Veins process %d did not shut down gracefully, sennding kill.",
            process.pid,
        )
        process.kill()
        try:
            process.wait(gracetime_s)
        except subprocess.TimeoutExpired as _exc2:
            logging.error(
                "Veins process %d could not even be killed!", process.pid
            )
    assert (
        process.poll() and process.returncode is not None
    ), "Veins could not be killed."


def serialize_action_discete(action):
    """Serialize a single discrete action into protobuf wire format."""
    reply = veinsgym_pb2.Reply()
    reply.action.discrete.value = action
    return reply.SerializeToString()


def parse_space(space):
    """Parse a Gym.spaces.Space from a protobuf request into python types."""
    if space.HasField("discrete"):
        return space.discrete.value
    if space.HasField("box"):
        return np.array(space.box.values, dtype=np.float32)
    if space.HasField("multi_discrete"):
        return np.array(space.multi_discrete.values, dtype=int)
    if space.HasField("multi_binary"):
        return np.array(space.multi_binary.values, dtype=bool)
    if space.HasField("tuple"):
        return tuple(parse_space(subspace) for subspace in space.tuple.values)
    if space.HasField("dict"):
        return {
            item.key: parse_space(item.value) for item in space.dict.values
        }
    raise RuntimeError("Unknown space type")


class VeinsEnv(gym.Env):
    metadata = {"render.modes": []}

    def __init__(
        self,
        scenario_dir=None,
        executable='run',
        env_path=None,
        run_veins=True,
        port=None,
        timeout=3.0,
        print_veins_stdout=False,
        action_serializer=serialize_action_discete,
        more_kwargs=None,
        user_interface="Cmdenv",
        sim_time_limit="1s",
        config="General",
    ):
        assert ensure_valid_scenario_dir(scenario_dir)
        self.scenario_dir = scenario_dir

        self.executable_path = executable
        if not os.path.isfile(self.executable_path):
            self.executable_path = os.path.join(os.path.dirname(scenario_dir), 'src', executable)

        self.env_path = env_path
        
        self._action_serializer = action_serializer

        self.action_space = SENTINEL_EMPTY_SPACE
        self.observation_space = SENTINEL_EMPTY_SPACE

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.port = port
        self.bound_port = None
        self._timeout = timeout
        self.print_veins_stdout = print_veins_stdout

        self.run_veins = run_veins
        self._passed_args = (
            more_kwargs if more_kwargs is not None else dict()
        )
        self._user_interface = user_interface
        self.sim_time_limit = sim_time_limit
        self._config = config
        self._seed = 0
        self.veins = None
        self._veins_shutdown_handler = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    # Gym Env interface

    def step(self, action):
        """
        Run one timestep of the environment's dynamics.
        """
        self.socket.send(self._action_serializer(action))
        step_result = self._parse_request(self._recv_request())
        if step_result.done:
            self.socket.send(
                self._action_serializer(self.action_space.sample())
            )
            logging.debug("Episode ended")
            if self.veins:
                logging.debug("Waiting for veins to finish")
                self.veins.wait()
        assert self.observation_space.contains(step_result.observation)
        return step_result

    def reset(self, seed=SENTINEL_NO_SEED_GIVEN, return_info=False, options=None):
        """
        Start and connect to a new veins experiment, return first observation.

        Shut down exisiting veins experiment processes and connections.
        Waits until first request from veins experiment has been received.
        """
        del options  # currently not used/implemented

        self.close()
        self.socket = self.context.socket(zmq.REP)
        if self.port is None:
            self.bound_port = self.socket.bind_to_random_port(
                "tcp://127.0.0.1"
            )
            logging.debug("Listening on random port %d", self.bound_port)
        else:
            self.socket.bind(f"tcp://127.0.0.1:{self.port}")
            self.bound_port = self.port
            logging.debug("Listening on configured port %d", self.bound_port)

        if seed is not SENTINEL_NO_SEED_GIVEN:
            self.seed(seed)

        if self.run_veins:
            self.veins = launch_veins(
                self.scenario_dir,
                self.executable_path,
                self.env_path,
                self._seed,
                self.bound_port,
                self.print_veins_stdout,
                self._passed_args,
                self._user_interface,
                self.sim_time_limit,
                self._config,
            )
            logging.info("Launched veins experiment, waiting for request.")

            def veins_shutdown_handler(signum=None, stackframe=None):
                """
                Ensure that veins always gets shut down on python exit.

                This is implemented as a local function on purpose.
                There could be more than one VeinsEnv in one python process.
                So calling atexit.unregister(shutdown_veins) could cause leaks.
                """
                shutdown_veins(self.veins)
                if signum is not None:
                    sys.exit()

            atexit.register(veins_shutdown_handler)
            signal.signal(signal.SIGTERM, veins_shutdown_handler)
            self._veins_shutdown_handler = veins_shutdown_handler

        initial_request = self._parse_request(self._recv_request())[0]
        logging.info("Received first request from Veins, ready to run.")
        if return_info:
            logging.warning("return info not yet implemented for reset()")
            initial_info = None  # not implemented
            return initial_request, initial_info

        return initial_request, dict()

    def render(self, mode="human"):
        """
        Render current environment (not supported by VeinsEnv right now).
        """
        raise NotImplementedError(
            "Rendering is not implemented for this VeinsGym"
        )

    def close(self):
        """
        Close the episode and shut down veins scenario and connection.
        """
        logging.info("Closing VeinsEnv.")
        if self._veins_shutdown_handler is not None:
            atexit.unregister(self._veins_shutdown_handler)

        if self.veins:
            # TODO: send shutdown message (which needs to be implemted in veins code)
            shutdown_veins(self.veins)
            self.veins = None

        if self.bound_port:
            logging.debug("Closing VeinsEnv server socket.")
            self.socket.unbind(f"tcp://127.0.0.1:{self.bound_port}")
            self.socket.close()
            self.socket = None
            self.bound_port = None
            self.veins = None

    def seed(self, seed=None):
        """
        Set and return seed for the next episode.

        Will generate a random seed if None is passed.
        """
        if seed is not None:
            logging.debug("Setting given seed %d", seed)
            self._seed = seed
        else:
            random_seed = gym.utils.seeding.create_seed(max_bytes=4)
            logging.debug("Setting random seed %d", random_seed)
            self._seed = seed
        return [self._seed]

    # Internal helpers

    def _recv_request(self):
        rlist, _, _ = zmq.select([self.socket], [], [], timeout=self._timeout)
        if not rlist:
            logging.error(
                "Veins instance with PID %d timed out after %.2f seconds",
                self.veins.pid,
                self._timeout,
            )
            raise TimeoutError(
                f"Veins instance did not send a request within {self._timeout}"
                " seconds"
            )
        assert rlist == [self.socket]
        return self.socket.recv()

    def _parse_request(self, data):
        request = veinsgym_pb2.Request()
        request.ParseFromString(data)
        if request.HasField("shutdown"):
            return StepResult(self.observation_space.sample(), 0.0, True, False, {})
        if request.HasField("init"):
            # parse spaces
            self.action_space = eval(request.init.action_space_code)
            self.observation_space = eval(request.init.observation_space_code)
            # sent empty reply
            init_msg = veinsgym_pb2.Reply()
            self.socket.send(init_msg.SerializeToString())
            # request next request (actual request with content)
            real_data = self._recv_request()
            real_request = veinsgym_pb2.Request()
            real_request.ParseFromString(real_data)
            # continue processing the real request
            request = real_request
        # the gym needs to be initialized at this point!
        assert self.action_space is not SENTINEL_EMPTY_SPACE
        assert self.observation_space is not SENTINEL_EMPTY_SPACE
        observation = parse_space(request.step.observation)
        reward = parse_space(request.step.reward)
        info = parse_space(request.step.info) if request.step.HasField('info') else {}
        assert len(reward) == 1
        return StepResult(observation, reward[0], False, False, info)
