from mancala import mancala_v1 as mancala
import copy
import random
import numpy as np

MAX_DEPTH = 6
AGENTS = ["player_0", "player_1"]

# Ideas
### Thread top level?
### needs to take fastest win where possible
### Check if pit score is over 24 and return inf
# Finished
### Add memo system to avoid double score calculations (eh)

def agent_function(env, agent):
    searchable_env = copy.deepcopy(env)
    pieces_on_board = 0
    
    global MEMO
    global MY_SIDE
    MEMO = {"1": 0}
    if agent == AGENTS[0]:
        MY_SIDE = 1
    else:
        MY_SIDE = 2
        
    observation, reward, termination, truncation, info = env.last()
    action = None
    if not (termination or truncation):
        best_move = [-1, float("-inf")]
        for possible_action in mancala.MancalaModel.ACTIONS(env.my_state):
            env1 = copy.deepcopy(searchable_env)
            env1.step(possible_action)
            if env1.my_state.turn == MY_SIDE:
                val = MAX(env1, 1)
            else:
                val = MIN(env1, 2)
            print(f"Action: {possible_action} Score: {val}")
            if val == float("inf"):
                return possible_action
            if val > best_move[1]:
                best_move = [possible_action, val]
        if best_move[0] == -1:
            action = random.choice(mancala.MancalaModel.ACTIONS(env.my_state))
        else:
            action = best_move[0]
    print(f"Dups vs total: {MEMO['1']}/{len(MEMO)}")
    return action

def MAX(env, depth):
    winning_score = IS_WINNING_HEURISTIC(env)
    if depth >= MAX_DEPTH:
        return EVALUATE(env)
    elif winning_score is not None:
        return winning_score
    v_max = float('-inf')
    for possible_action in mancala.MancalaModel.ACTIONS(env.my_state):
        env1 = copy.deepcopy(env)
        env1.step(possible_action)
        if env1.my_state.turn == MY_SIDE:
            v = MAX(env1, depth)
        else:
            v = MIN(env1, depth+1)            
        if v > v_max:
            v_max = v
            if v == float("inf"):
                break
    return v_max
    

def MIN(env, depth):
    winning_score = IS_WINNING_HEURISTIC(env)
    if depth >= MAX_DEPTH:
        return EVALUATE(env)
    elif winning_score is not None:
        return winning_score
    v_min = float('inf')
    for possible_action in mancala.MancalaModel.ACTIONS(env.my_state):
        env1 = copy.deepcopy(env)
        env1.step(possible_action)
        if env1.my_state.turn == MY_SIDE:
            v = MAX(env1, depth+1)
        else:
            v = MIN(env1, depth)
        if v < v_min:
            v_min = v
            if v == float("-inf"):
                break
    return v_min

def EVALUATE(env):
    env_string = mancala.MancalaModel.STRINGIFY_STATE(env.my_state)
    if env_string in MEMO:
        MEMO["1"] += 1
        return MEMO[env_string]

    final_reward = 0

    if MY_SIDE == 1:
        my_pits = env.my_state.observation[:env.my_state.size//2]
        other_pits = env.my_state.observation[env.my_state.size//2:]
    else:
        my_pits = env.my_state.observation[env.my_state.size//2:]
        other_pits = env.my_state.observation[:env.my_state.size//2]

    if my_pits[-1] > 24:
        final_reward = float("inf")
        MEMO[env_string] = final_reward
        return final_reward
    elif other_pits[-1] > 24:
        final_reward = float("-inf")
        MEMO[env_string] = final_reward
        return final_reward


    # Add up all the pieces on the board
    for pit in my_pits[:-1]:
        final_reward += pit
        
    for pit in other_pits[:-1]:
        final_reward -= pit

    final_reward += (my_pits[-1] - other_pits[-1]) * 5

    MEMO[env_string] = final_reward

    return final_reward

def IS_WINNING_HEURISTIC(env):
    if MY_SIDE == 1:
        my_store = env.my_state.observation[env.my_state.size//2-1]
        other_store = env.my_state.observation[env.my_state.size-1]
    else:
        other_store = env.my_state.observation[env.my_state.size//2-1]
        my_store = env.my_state.observation[env.my_state.size-1]

    if my_store > 24:
        return float("inf")
    elif other_store > 24:
        return float("-inf")
    else:
        return None