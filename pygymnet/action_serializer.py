from . import veinsgym_pb2

# Function to serialize action dictionary to protobuf message
def my_action_serializer(action):
    reply = veinsgym_pb2.Reply()
    example_action = action['example_action']  # Example: torch tensor of shape (10,)

    # Add serialized action to the protobuf message
    item = reply.action.dict.values.add()
    item.key = "example_action"
    item.value.box.values.extend(example_action)
    
    return reply.SerializeToString()