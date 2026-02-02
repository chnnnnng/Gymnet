#include "ExampleGymProcess.h"
#include "../GymConnection/GymConnection.h"

Define_Module(ExampleGymProcess);

using namespace omnetpp;

#define TTI 0.1 // 100 ms

void ExampleGymProcess::initialize(int stage)
{
    gym_connection = reinterpret_cast<GymConnection *>(getParentModule()->getSubmodule("gym_connection"));
    ttiEvent = new cMessage("ttiEvent");
    scheduleAt(simTime() + TTI, ttiEvent);
}

void ExampleGymProcess::handleMessage(cMessage *msg)
{
    if (msg == ttiEvent)
    {
        scheduleAt(simTime() + TTI, ttiEvent); // Schedule next TTI

        // Example: send a dummy observation to Gym every TTI
        veinsgym::proto::Request request;
        request.set_id(1); // Example ID

        // Construct a dummy observation
        auto *obsDict = request.mutable_step()->mutable_observation()->mutable_dict();
        auto *obsItem = obsDict->add_values();
        obsItem->set_key("example_obskey");
        auto *exampleBox = obsItem->mutable_value()->mutable_box();
        for (int i = 0; i < 10; ++i)
        {
            exampleBox->add_values(static_cast<double>(i)); // Example observation values
        }

        // Construct a dummy reward
        request.mutable_step()->mutable_reward()->mutable_box()->add_values(1.0); // Example reward

        // Send the request to Gym
        auto reply = gym_connection->communicate(request);
        EV << "[ExampleGymProcess] Sent observation to Gym." << endl;

        // Process the reply from Gym
        auto &reply_dict = reply.action().dict();
        for (const auto &item : reply_dict.values())
        {
            if (item.key() == "example_action")
            {
                const auto &vals = item.value().box().values();
                EV << "[ExampleGymProcess] Received action from Gym: ";
                for (double v : vals)
                    EV << v << " ";
                EV << endl;
            }
        }
    }
    else
    {
        EV << "[ExampleGymProcess] Received message: " << msg->getName() << endl;
        delete msg;
    }
}