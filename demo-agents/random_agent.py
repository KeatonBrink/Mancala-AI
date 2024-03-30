import random
from mancala import mancala_v1 as mancala

def agent_function(env, agent):
    observation, reward, termination, truncation, info = env.last()

    action = None
    if not (termination or truncation):
        # this is where you would insert your policy
        actions = mancala.MancalaModel.ACTIONS(env.my_state)
        action = random.choice(actions)


    return action

def main():
    env = mancala.env(render_mode="ansi")
    env.reset(seed=42)

    for agent in env.agent_iter():
        env.step(agent_function(env, agent))
    print(f"Winner: {env.winner}")
    env.close()

if __name__ == "__main__":
    main()