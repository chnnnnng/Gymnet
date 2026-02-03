# Gymnet
An OMNeT++ project with Gymnasium integration for reinforcement learning simulations.

## Getting Started

Clone the repository to your local machine:
```bash
git clone <repository_url>
```
This will create a folder, e.g., `somewhere/Gymnet`.

## Setting Up the OMNeT++ Environment

### Download Dependencies

1. Download `zeromq-4.3.5.zip` from the [ZMQ Releases page](https://github.com/zeromq/libzmq/releases/tag/v4.3.5).
2. Extract it to: `somewhere/Gymnet/Gymnet-addition/zeromq-4.3.5`.
3. Download `protobuf-cpp-3.1.0.zip` from the [Protobuf Releases page](https://github.com/protocolbuffers/protobuf/releases/tag/v3.1.0).
4. Extract it to: `somewhere/Gymnet/protobuf-3.1.0`.

### Build Dependencies

Open the OMNeT++ Shell and navigate to `somewhere/Gymnet/Gymnet-addition`.

Run the following command:
```bash
make all -j$(nproc)
```
This will automatically build `zmq`, `protobuf`, `gymnet-inet4`, and `gymnet-lte`.

You can also build each component separately:
```bash
make zmq
make protobuf
make gymnet-inet4
make gymnet-lte
```

To clean the build artifacts, use:
```bash
make cleanall
make clean-zmq
make clean-protobuf
make clean-gymnet-inet4
make clean-gymnet-lte
```

Upon successful build, new files will be available in `Gymnet-addition/include`, `Gymnet-addition/bin`, and `Gymnet-addition/lib`.

### Build the Demo Project

Open the OMNeT++ Shell and navigate to `somewhere/Gymnet/Gymnet`.

Run:
```bash
make cleanall
make makefiles
make all -j$(nproc)
```

If successful, an executable (`Gymnet` or `Gymnet.exe`) will be generated in `somewhere/Gymnet/Gymnet/src`.

> **Note:** `make makefiles` is only required for the first build. For subsequent builds, `make all` suffices.

## Setting Up the Gym Script

### Install Requirements

Create and activate a Conda or virtual environment.

Install required packages:
```bash
pip install -r requirements.txt
```

### Link Gym with Gymnet

Open `pygymnet/config.py` and configure the following:
- `omnetpp_installation_dir`
- `gymnet_addition_dir`
- `scenario_dir`
- `executable`
- `config_name`
- `time_limit`

> For the demo simulation (project: `Gymnet`, executable: `Gymnet`, config: `demo`), only `omnetpp_installation_dir` and `gymnet_addition_dir` need to be configured.

### Run the Python Script

A demo script (`demo.py`) is provided. Run it with:
```bash
python demo.py
```

> Ensure your Python environment is activated.
> If you encounter the error `"module 'numpy' has no attribute 'bool8'"`, replace all `np.bool8` with `np.bool` in `site-packages/gym/utils/passive_env_checker.py`.

### Demo Code Overview

```python
import gym
import pygymnet

env = gym.make("gymnet-v1")
env.seed(0)

observation = env.reset()
done = False
while not done:
    action = env.action_space.sample()
    observation, reward, done, truncated, info = env.step(action)
    example_obs = observation['example_obskey']
    if not done:
        print(f"Gym chose Action: {action['example_action']}")
        print(f"Received observation: {example_obs} and reward: {reward}")
```

This demonstrates the observation-action-reward loop, which continues until `done` is `True` (e.g., when the simulation reaches the `time_limit` set in `config.py`).

## Customizing for Your Project

- **OMNeT++ Project**:
  - Create a new OMNeT++ project based on `Gymnet` (overwrite or copy it).
  - Implement your own `ExampleGymProcess`.
  - Build a network containing your custom GymProcess.
  - Edit `omnetpp.ini` to correctly configure `*.gym_connection.observation_space` and `*.gym_connection.action_space`.
  - Build the OMNeT++ project.

- **Python Code**:
  - Customize your Python code based on `demo.py`. For reinforcement learning, use an agent to decide actions based on observations.
  - Update `pygymnet/config.py` to match your OMNeT++ project settings.
  - Implement `pygymnet/action_serializer.py` to align with `*.gym_connection.action_space`.

## Simulating Gymnet-NR

A basic **OMNeT + LTE/NR + Gym** workflow is provided. Dependencies are included in `Gymnet-addition`:
- **Gymnet-inet4**: A minimal version for INET 4.2.2 (can be used instead of the original INET).
- **Gymnet-lte**: A modified version for SimuLTE 1.2.0 (do not use the original SimuLTE).

> The OMNeT++ + LTE/NR + Gym workflow has been tested on **OMNeT++ Versions 5.6.2 and 6.1** (available from https://omnetpp.org/download/old).

### Build gymnet-inet4 and gymnet-lte

The `make all` command in the [Build dependencies](#build-dependencies) section automatically builds `gymnet-inet4` and `gymnet-lte`. To rebuild them, run:
```bash
make clean-gymnet-inet4 && make gymnet-inet4
make clean-gymnet-lte && make gymnet-lte
```

Upon success, you will find `libINET` in `gymnet-inet4/src` and `libGYMNETLTE` in `gymnet-lte/src`.

These libraries are required to enable LTE/NR features in your OMNeT++ project. The standard [build commands](#build-the-demo-project) will not link them automatically. Use the following instead:
   ```bash
   make cleanall
   make makefiles ENABLE_NR=TRUE
   make all -j$(nproc)
   ```
`ENABLE_NR=TRUE` ensures the linker uses the correct paths for `libINET` and `libGYMNETLTE`. If using a custom `Makefile`, ensure proper `-I`, `-L`, and `-l` options.

## Final Notes

We hope this project supports your studies and research! For assistance, feel free to reach out.
```