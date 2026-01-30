# Gymnet
OMNet++ project with Gymnasium connection.

## Getting Started

Clone the repository to your computer:
```
git clone <repository_url>
```
This will create a folder, e.g., `somewhere/Gymnet`.

## Preparing the OMNet++ Environment

### Build and Install ZMQ (libzmq)

1. Download `zeromq-4.3.5.zip` from [ZMQ Releases](https://github.com/zeromq/libzmq/releases/tag/v4.3.5).
2. Extract it to the Gymnet folder: `somewhere/Gymnet/zeromq-4.3.5`.
3. Open the OMNet++ Shell and navigate to `somewhere/Gymnet/zeromq-4.3.5`.
4. Run the following commands:
   ```
   ./configure
   make
   make install
   ```

### Build and Install Protobuf 3.20.0

1. Download `protobuf-cpp-3.20.0.zip` from [Protobuf Releases](https://github.com/protocolbuffers/protobuf/releases/tag/v3.20.0).
2. Extract it to the Gymnet folder: `somewhere/Gymnet/protobuf-3.20.0`.
3. Open the OMNet++ Shell and navigate to `somewhere/Gymnet/protobuf-3.20.0`.
4. Run the following commands:
   ```
   ./configure CXXFLAGS="-std=c++17"
   make
   make install
   ```

> To uninstall `libzmq` or `libprotobuf`, use `make uninstall`.

### Build the OMNet++ Project (Linking with libzmq and libprotobuf)

#### Using OMNet++ IDE

1. Right-click the project (e.g., `Gymnet`) and select `Properties`.
2. Navigate to `OMNet++` -> `Makemake`.
3. Select `src: makemake` and click `Options`.
4. Under `Link`, click `More>>`.
5. Add `zmq` and `protobuf` to `Additional libraries to link with`.
6. Click `OK`, then `Apply and Close`. Finally, build or rebuild the project.

> Steps 1–5 are only required for the first build.  
> If the build fails, delete the `Makefile` in the `src` folder and rebuild.

#### Using OMNet++ Shell (**Recommended**)

1. Open the OMNet++ Shell and navigate to `somewhere/Gymnet/Gymnet`.
2. Run the following commands:
   ```
   make cleanall
   make makefiles
   make all
   ```

> `make makefiles` is only required for the first build. For subsequent builds, only `make all` is needed.  
> If issues occur during subsequent builds, repeat `cleanall` and `makefiles` before running `make all`.

If the build succeeds, you will find an executable file (`Gymnet` or `Gymnet.exe`) in `somewhere/Gymnet/Gymnet/src`.

## Preparing the Gym Script

### Install Requirements

1. Create and activate a `.conda` or `.venv` environment.
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Link Gym with Gymnet

1. Open `pygymnet/config.py` and configure the following items:
   - `omnetpp_installation_dir`
   - `scenario_dir`
   - `executable`
   - `config_name`
   - `time_limit`
2. Open `pygymnet/action_serializer.py` and implement your action serializer.

> For the demo simulation (project name: `Gymnet`, executable name: `Gymnet`, config name: `demo`), you only need to configure `omnetpp_installation_dir`.

### Run the Python Script

A simple demo script (`demo.py`) is provided. Run it as follows:
```
python demo.py
```

> Ensure the correct `.conda` or `.venv` environment is activated.  
> If you encounter the error `"module 'numpy' has no attribute 'bool8'"`, replace all occurrences of `np.bool8` with `np.bool` in `site-packages/gym/utils/passive_env_checker.py`.

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

This code demonstrates the observation-action-reward loop until `done` is `True` (e.g., when the simulation time reaches `time_limit` in `pygymnet/config.py`).

## Customizing for Your Project

- **OMNet++ Project**:
  - Create a new OMNet++ project based on `Gymnet` (overwrite or copy it).
  - Implement your own `ExampleGymProcess`.
  - Build a network with your custom GymProcess.
  - Edit `omnetpp.ini` to ensure `*.gym_connection.observation_space` and `*.gym_connection.action_space` are correctly configured.
  - Build the OMNet++ project.

- **Python Code**:
  - Customize your Python code based on `demo.py`. For reinforcement learning, use an agent to make actions based on observations.
  - Update `pygymnet/config.py` to match your OMNet++ project.
  - Implement `pygymnet/action_serializer.py` to match `*.gym_connection.action_space`.

## Final Notes

May this project assist you in your studies and research! If you need help, feel free to contact me.