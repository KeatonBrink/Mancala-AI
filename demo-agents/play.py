import random
from mancala import mancala_v1 as mancala
import time
import copy
import sys
import minimax_agent
# import best_agent_alpha_beta
import random_agent
import human_agent
import alpha_beta_agent
import go_alpha_beta_agent

TEST = False

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "go_human0":
            agent_function = { "player_0": human_agent.agent_function, "player_1": go_alpha_beta_agent.agent_function }
        elif sys.argv[1] == "go_human1":
            agent_function = { "player_0": go_alpha_beta_agent.agent_function, "player_1": human_agent.agent_function }
        elif sys.argv[1] == "go_robots":
            agent_function = { "player_0": go_alpha_beta_agent.agent_function, "player_1": go_alpha_beta_agent.agent_function }
        elif sys.argv[1] == "py_human0":
            agent_function = { "player_0": human_agent.agent_function, "player_1": alpha_beta_agent.agent_function }
        elif sys.argv[1] == "py_human1":
            agent_function = { "player_0": alpha_beta_agent.agent_function, "player_1": human_agent.agent_function }
        elif sys.argv[1] == "py_robots":
            agent_function = { "player_0": alpha_beta_agent.agent_function, "player_1": alpha_beta_agent.agent_function }
        else:
            print("Invalid argument. Valid arguments are: human0, human1, go_robots, py_robots")
            return
    else:
        agent_function = { "player_0": go_alpha_beta_agent.agent_function, "player_1": go_alpha_beta_agent.agent_function }
    # agent_function = { "player_0": minimax_agent.agent_function, "player_1": human_agent.agent_function }
    # agent_function = { "player_0": human_agent.agent_function, "player_1": minimax_agent.agent_function }
    # agent_function = { "player_0": alpha_beta_agent.agent_function, "player_1": go_alpha_beta_agent.agent_function }
    # agent_function = { "player_0": minimax_agent.agent_function, "player_1": minimax_agent.agent_function }
    # agent_function = { "player_0": minimax_agent.agent_function, "player_1": alpha_beta_agent.agent_function }
    # agent_function = { "player_0": random_agent.agent_function, "player_1": minimax_agent.agent_function }
    times = { "player_0": 0.0, "player_1": 0.0 }

    # env = connect_four_v3.env(render_mode="human")
    env = mancala.env(render_mode=None)
    env.reset()

    for agent in env.agent_iter():
        if True:
            """text display of board"""
            print(env.my_state)
            print()
            print()
            print()
        t1 = time.time()
        action = agent_function[agent](env, agent)
        t2 = time.time()
        times[agent] += (t2-t1)

        env.step(action)
        try:
            observation, reward, termination, truncation, info = env.last()
            print("{} took action {}".format(agent, action))
            if termination or truncation:
                winner = env.winner
                if winner != -1:
                    print(f"Player_{winner} wins.")
                else:
                    print("Both lost.")
                if True:
                    """text display of board"""
                    print(env.my_state)
                    print()
                    print()
                    print()
                break
        except:
            pass

    # time.sleep(10) # useful for end of game with human render mode
    env.close()

    for agent in times:
        print(f"{agent} took {times[agent]:8.5f} seconds.")
    return (winner, times["player_1"])

if __name__ == "__main__":
    if False:
        import cProfile
        cProfile.run('main()')
    elif TEST:
        test_count = 20
        failed_tests = 0
        time_taken = 0
        for i in range(test_count):
            main_results = main()
            time_taken += main_results[1]
            if main_results[0] != 1:
                failed_tests += 1
        print(f"After {test_count} tests, Player 1 lost {failed_tests}, with average time of {(time_taken / test_count):8.5f}")

    else:
        main()