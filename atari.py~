import gym
env = gym.make('SpaceInvaders-v0')
env.reset()
score = 0
print(env.action_space)
print(env.observation_space)
while True:    
    env.render()
    observation, reward, done, info = env.step(5) # take a random action
    score += reward
    if done:
        print done, score
	score = 0
        env.reset()
