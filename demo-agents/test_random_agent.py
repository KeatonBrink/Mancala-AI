import random
from mancala import mancala_v1 as mancala

wins_1 = 0
for i in range(1000):
    env = mancala.env()
    env.reset(seed=42)

    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        action = None
        if not (termination or truncation):
            # this is where you would insert your policy
            actions = mancala.MancalaModel.ACTIONS(env.my_state)
            action = random.choice(actions)


        env.step(action)
    print(f"Winner: {env.winner}")
    if env.winner == 0:
        wins_1 += 1
    env.close()

print(f"Player 1 won {wins_1} times")