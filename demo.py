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
      print(f"Gym choose Action: {action['example_action']}")
      print(f"Get observation: {example_obs} and reward {reward}")
print("OMNet++ simulation end.")