from mancala import mancala_v1 as mancala
import minimax_agent

def main():
    # board = [0, 0, 0, 0, 8, 3, 22, 0, 0, 1, 0, 0, 0, 14]
    # env = mancala.env(render_mode=None)
    # env.reset()
    # env.my_state.observation = board
    # env.my_state.turn = 2
    # print(minimax_agent.agent_function(env, "player_1"))

    board = [6, 6, 1, 0, 8, 0, 7, 2, 1, 7, 6, 0, 1, 3]
    env = mancala.env(render_mode=None)
    env.reset()
    env.my_state.observation = board
    env.my_state.turn = 1
    env.step(4)
    print(env.agent_selection)

if __name__ == "__main__":
    main()