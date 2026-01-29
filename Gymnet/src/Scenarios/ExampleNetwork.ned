package gymnet.Scenarios;
import gymnet.GymConnection.GymConnection;
import gymnet.ExampleGymProcess.ExampleGymProcess;

network ExampleNetwork
{
    submodules:
        gym_connection: GymConnection;
        gym_process: ExampleGymProcess;
    connections allowunconnected:
}