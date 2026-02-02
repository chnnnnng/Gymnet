from . import veinsgym_pb2
import numpy as np

# This is a simple serializer that converts a dictionary of actions
# it actually works quite well for most use cases (Dict action with box contents)
# you don't need to modify this unless you have a very specific action format
def my_action_serializer(action):
    reply = veinsgym_pb2.Reply()
    
    for action_key, action_value in action.items():
        item = reply.action.dict.values.add()
        item.key = action_key
        
        if isinstance(action_value, (list, tuple, np.ndarray)):
            item.value.box.values.extend(action_value)
        else:
            item.value.box.values.append(action_value)
    
    return reply.SerializeToString()