from mancala import mancala_v1 as mancala
import copy
import random
import numpy as np
import subprocess

AGENTS = ["player_0", "player_1"]
GO_AGENT = "./go_agent/go_agent"

def agent_function(env, agent):
    observation, reward, termination, truncation, info = env.last()
    if termination or truncation:
        return None
    try:
        result = subprocess.run([GO_AGENT], input=mancala.MancalaModel.STRINGIFY_STATE(env.my_state), check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
        if result.stderr != "":
            print("STDERR:")
            print(result.stderr)
        # print(result.returncode)
        return int(result.returncode)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        return env.my_state.ACTIONS()[0]