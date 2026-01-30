########################## User Configuration ##########################

# where is your omnet++ installation directory
omnetpp_installation_dir = r"C:\Users\chng\Warehouse\omnetpp-6.1"

# where is the omnetpp.ini file located
scenario_dir = "Gymnet/simulations"

# what is the name of your omnetpp simulation executable (if something went wrong, try absolute path here)
executable = "Gymnet"

# what is the name of your omnetpp.ini configuration to run
config_name = "demo"

# for how long the simulation should run
time_limit = "500ms"




############################# Advanced Configuration ##########################
# Do not modify the following parameters unless you know what you're doing.

import platform
from .action_serializer import my_action_serializer

gymnet_config = {
    "scenario_dir": scenario_dir,  # Directory where omnetpp.ini is located
    "executable": executable,  # OMNet++ simulation executable name or absolute path
    "config": config_name,  # omnetpp.ini configuration name
    "sim_time_limit": time_limit,  # Simulation time limit
    "run_veins": True,  # Whether to run the OMNet++ simulation
    "print_veins_stdout": False,  # Print OMNet++ simulation stdout (useful for debugging)
    "user_interface": "Cmdenv",  # User interface: "Cmdenv" or "Qtenv"
    "port": None,  # Port for OMNet++ simulation connection (None for random port)
    "timeout": 1,  # Timeout for connecting to the simulation
    "action_serializer": my_action_serializer,  # Function to serialize actions to protobuf
    "more_kwargs": {
        # '--example_key': "example_value",  # Additional command-line arguments
    },
    # Environment path for Windows users (required for OMNet++ to run properly)
    "env_path": (
        f"{omnetpp_installation_dir}\\tools\\win32.x86_64\\opt\\mingw64\\bin;"
        f"{omnetpp_installation_dir}\\tools\\win32.x86_64\\mingw64\\bin;"
        f"{omnetpp_installation_dir}\\bin;"
        if platform.system() == "Windows" else None
    ),
}

# Enable logging for debugging
import logging
logging.basicConfig(level=logging.WARNING)