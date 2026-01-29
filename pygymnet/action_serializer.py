from . import veinsgym_pb2

# a function to serialize action dict to protobuf message
def my_action_serializer(action):
    reply = veinsgym_pb2.Reply()
    example_action = action['example_action'] # torch tensor of shape (10,)

    item = reply.action.dict.values.add()
    item.key = "example_action"
    item.value.box.values.extend(example_action)
    
    return reply.SerializeToString()