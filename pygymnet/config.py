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
# if you are not professional user, do not change the following parameters
import platform
from .action_serializer import my_action_serializer
gymnet_config = {
    "scenario_dir": scenario_dir, # directory where omnetpp.ini is located
    "executable": executable, # omnet++ simulation executable name or absolute path
    "config": config_name, # omnetpp.ini configuration name
    "sim_time_limit": time_limit, # simulation time limit
    "run_veins": True, # whether to run the omnet++ simulation
    "print_veins_stdout": False, # whether to print the stdout of the omnet++ simulation (can be useful for debugging)
    "user_interface": "Cmdenv", # the user interface, can be "Cmdenv" or "Qtenv" (simulation will not start automatically in Qtenv)
    "port": None, # port for the omnet++ simulation to connect to, None for random port
    "timeout": 1, # timeout for connecting to the simulation
    "action_serializer": my_action_serializer, # function to serialize action dict to protobuf message (you need to implement this function yourself)
    "more_kwargs": {
        # '--example_key': "example_value",  # more command line arguments to pass to the simulation
    },
    
    # [For Windows users only] some environment path should be set for omnet++ to run properly, check README for more details
    "env_path": f"{omnetpp_installation_dir}\\tools\\win32.x86_64\\opt\\mingw64\\bin;{omnetpp_installation_dir}\\tools\\win32.x86_64\\mingw64\\bin;{omnetpp_installation_dir}\\bin;" if platform.system() == "Windows" else None,
}

# enable logging for debugging
import logging
logging.basicConfig(level=logging.WARNING)