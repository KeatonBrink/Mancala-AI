import random
from mancala import mancala_v1 as mancala

def agent_function(env, agent):
    observation, reward, termination, truncation, info = env.last()

    action = None
    if not (termination or truncation):
        # this is where you would insert your policy
        actions = mancala.MancalaModel.ACTIONS(env.my_state)
        print("Possible actions:")
        print(actions)
        action = int(input("Choose action: "))


    return action