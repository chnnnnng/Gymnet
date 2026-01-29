# Gymnet
OMNet++ project with Gymnasium connection.

## Get Ready

`git clone` somewhere on your computer, you will have 'somewhere/Gymnet'.

## Prepare your OMNet++ environment

### Make and install ZMQ (libzmq)

1. Download zeromq-4.3.5.zip from https://github.com/zeromq/libzmq/releases/tag/v4.3.5
2. Unzip to Gymnet folder: somewhere/Gymnet/zeromq-4.3.5
3. Run OMNet++ Shell and cd to somewhere/Gymnet/zeromq-4.3.5
4. Then, do `./configure`, `make` and `make install`

### Make and install Protobuf 3.20.0

1. Download protobuf-cpp-3.20.0.zip from https://github.com/protocolbuffers/protobuf/releases/tag/v3.20.0
2. Unzip to Gymnet folder: somewhere/Gymnet/protobuf-3.20.0
3. Run OMNet++ Shell and cd to somewhere/Gymnet/protobuf-3.20.0
4. Then, do `./configure CXXFLAGS="-std=c++17"`, `make` and `make install` 

> libzmq and libprotobuf can be uninstalled by `make uninstall`

### Build OMNet++ Project (linking with libzmq and libprotobuf)

Use OMNet++ IDE:

1. Right click your project ('Gymnet' for example) and enter 'Properties for Gymnet',
2. Find 'OMNet++' -> 'Makemake',
3. Select 'src: makemake', click 'options',
4. Select 'Link', click 'More>>',
5. Add two new entries in 'Additional libraries to link with': `zmq` and `protobuf`,
6. Clock 'Ok' and 'Apply and close', then `build` or `rebuild` your project.

> step 1 ~ 5 are only meant for fisrt time build.
> If build doesn't work, delete `Makefile` in `src` folder then rebuild again.

Use OMNet++ Shell (**Recommended**):

1. Run OMNet++ Shell and cd to somewhere/Gymnet/Gymnet
2. Do `make cleanall`
3. Do `make makefiles`
4. Do `make all`

> step 2 and 3 are meant for first build, for further build only step 4 is required.
> if something went wrong in further build, try step 2 and 3 before `make all`.

If build successfully, you may find a excutable file 'Gymnet' or 'Gymnet.exe' in 'somewhere/Gymnet/Gymnet/src'

## Prepare your Gym script

### Install requirements

1. Create a .conda or .venv environment and activate it,
2. Install requirements by `pip install -r requirements.txt`.

### Link Gym with Gymnet

1. Goto 'pygymnet/config.py', edit config items, including `omnetpp_installation_dir`,`scenario_dir`,`executable`,`config_name`,`time_limit`,
2. Goto 'pygymnet/action_serializer.py', implement your action serializer.

> if you only want to run the demo simulation (project name and executable name is 'Gymnet', config name is 'demo'), simply edit `omnetpp_installation_dir` is ok.

### Run python script

a simple demo `demo.py` is given, you can run it now!

> make sure you are in correct conda/venv environment

> if you encounter with an error "module 'numpy' has no attribute 'bool8'", it's ok, you can just replace all `np.bool8` with `np.bool` in `site-packages\gym\utils\passive_env_checker.py`.

### Let's see the demo code

```
import gym
import pygymnet
```
You should import these packages first.

```
env = gym.make("gymnet-v1")
env.seed(0)
```
These line create a new env using gymnet-v1 and set random seed to 0.

```
observation = env.reset()
done = False
while not done:
    action = env.action_space.sample()
    observation, reward, done, truncated, info = env.step(action)
    example_obs = observation['example_obskey']
    if not done: 
      print(f"Gym choose Action: {action['example_action']}")
      print(f"Get observation: {example_obs} and reward {reward}")
```
Do 'observation-action-reward' loop, until done (in this case, simulation time reaches `time_limit` in `pygymnet/config.py`).

## For your own job

- Create new OMNet++ project based on `Gymnet` (you can overwrite it or write from a copy).
    - Specifically, you have to implement your own `ExampleGymProcess`
    - Build a network with your own GymProcess
    - Important, you have to edit `omnetpp.ini`, make sure `*.gym_connection.observation_space` and `*.gym_connection.action_space` is correct
    - Build OMNet++ project
- Manage your python code
    - Write your python code based on `demo.py`, if you want to do reinforcement learning, you need to use a agent to make actions based on observations.
    - Edit `pygymnet/config.py` correspinding to your own OMNet++ project
    - Implement `pygymnet/action_serializer.py` corresponding to `*.gym_connection.action_space`

## Last but not least

May this work help you in your study and research! If you need any help, feel free to contact me.