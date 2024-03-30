# import functools

import gymnasium
import numpy as np
from .mancala_model import MancalaState as mancala_state
from gymnasium.spaces import Discrete

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers

NUM_ITERS = 1000
# from mancala.envs.mancala_model import MancalaModel
# from mancala.envs.mancala_model import MancalaState

def env(render_mode=None):
    """
    The env function often wraps the environment in wrappers by default.
    You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    internal_render_mode = render_mode
    env = raw_env(render_mode=internal_render_mode)
    # This wrapper is only for environments which print results to the terminal
    # this wrapper helps error handling for discrete action spaces
    env = wrappers.AssertOutOfBoundsWrapper(env)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    return env

class raw_env(AECEnv):
    metadata = {'render.modes': ['ansi'], "name": "mancala_v0"}
    
    def __init__(self, render_mode=None):
        self.possible_agents = ["player_" + str(r) for r in range(2)]

        # optional: a mapping between agent name and ID
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )

        # optional: we can define the observation and action spaces here as attributes to be used in their corresponding methods
        self._action_spaces = {agent: Discrete(6) for agent in self.possible_agents}
        self._observation_spaces = {
            agent: Discrete(14) for agent in self.possible_agents
        }
        self.render_mode = render_mode

    @property
    def visible_state(self):
        return self.my_state
    
    def action_space(self, agent):
        return Discrete(6)

    # Hmmm
    def render(self):
        # """
        # Renders the environment. In human mode, it can print to terminal, open
        # up a graphical window, or open up some other display that a human can see and understand.
        # """
        # if self.render_mode is None:
        #     gymnasium.logger.warn(
        #         "You are calling render method without specifying any render mode."
        #     )
        #     return

        # if len(self.agents) == 2:
        #     string = "Current state: Agent1: {} , Agent2: {}".format(
        #         MOVES[self.state[self.agents[0]]], MOVES[self.state[self.agents[1]]]
        #     )
        # else:
        #     string = "Game over"
        # print(string)
        if self.render_mode == "ansi":
            print(self.my_state)
    
    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        # observation of one agent is the previous state of the other
        return self.my_state.observation
    
    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pass

    def reset(self, seed=None, options=None):
        """
        Reset needs to initialize the following attributes
        - agents
        - rewards
        - _cumulative_rewards
        - terminations
        - truncations
        - infos
        - agent_selection
        And must set up the environment so that render(), step(), and observe()
        can be called without issues.
        Here it sets up the state dictionary which is used by step() and the observations dictionary which is used by step() and observe()
        """
        self.agents = self.possible_agents[:]
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self.my_state = mancala_state()
        self.my_state.reset()
        # self.observations = {agent: self.state.observation for agent in self.agents}
        self.num_moves = 0
        """
        Our agent_selector utility allows easy cyclic stepping through the agents list.
        """
        # This is probably incorrect
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()
        self.winner = None

    def step(self, action):
        """
        step(action) takes in an action for the current agent (specified by
        agent_selection) and needs to update
        - rewards
        - _cumulative_rewards (accumulating the rewards)
        - terminations
        - truncations
        - infos
        - agent_selection (to the next agent)
        And any internal state used by observe() or render()
        """
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            # handles stepping an agent which is already dead
            # accepts a None action for the one agent, and moves the agent_selection to
            # the next dead agent,  or if there are no more dead agents, to the next live agent
            self._was_dead_step(action)
            return

        agent = self.agent_selection

        prev_agent = self.my_state.turn
        # stores action of current agent
        self.my_state.empty_pit(action)

        # self.observations = {agent: self.state.observation for agent in self.agents}

        if self.my_state.turn == prev_agent:
            self.render()
            return

        # collect reward if it is the last agent to act
        if self._agent_selector.is_last():
            # rewards for all agents are placed in the .rewards dictionary
            # self.rewards[self.agents[0]], self.rewards[self.agents[1]] = REWARD_MAP[
            #     (self.state[self.agents[0]], self.state[self.agents[1]])
            # ]
            self.rewards[self.agents[0]], self.rewards[self.agents[1]] = self.my_state.reward()

            self.num_moves += 1
            # The truncations dictionary must be updated for all players.
            self.truncations = {
                agent: self.num_moves >= NUM_ITERS for agent in self.agents
            }

            # observe the current state
            # for i in self.agents:
            #     self.observations[i] = self.my_state[
            #         self.agents[1 - self.agent_name_mapping[i]]
            #     ]
        else:
            # no rewards are allocated until both players give an action
            self._clear_rewards()

        # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        # Adds .rewards to ._cumulative_rewards
        self._accumulate_rewards()
        self.terminations = {
            agent: self.my_state.game_over() for agent in self.agents
        }
        if self.my_state.game_over():
            self.winner = self.my_state.winner
        self.render()

        

# # try:
# #     import pygame
# # except ImportError as e:
# #     raise DependencyNotInstalled(
# #         "pygame is not installed, `pip install` must have failed."
# #     ) from e

# class MancalaEnv(gymnasium.Env):

#     metadata = {
#         "render_modes": ["ansi"],
#         "render_fps": 1,
#     }

#     def __init__(self, render_mode=None, pit_count=6):
#         self.render_mode = render_mode
#         self.pit_count = pit_count * 2 + 2
#         self.action_space = spaces.Discrete(pit_count)
#         self.observation_space = spaces.Box(0, 1, shape=(pit_count,), dtype=np.int8)

#         # # display support
#         # self.cell_size = (800//coin_count, 60)
#         # self.window_size = (
#         #     self.coin_count * self.cell_size[0],
#         #     1 * self.cell_size[1],
#         # )
#         # self.window_surface = None
#         # self.clock = None
#         # self.head_color = (255, 0, 0)
#         # self.tail_color = (0, 0, 255)
#         # self.background_color = (170, 170, 170)
#         return

#     def reset(self, seed=None, options=None):
#         super().reset(seed=seed)
#         self.state = MancalaState(self.pit_count)
#         self.state.randomize(seed)

#         observation = self.state.observation
#         info = {}
#         return observation, info

#     def step(self, action):
#         state = self.state
#         state1 = MancalaModel.RESULT(state, action)
#         self.state = state1
        
#         observation = self.state.observation
#         reward = MancalaModel.STEP_COST(state, action, state1)
#         terminated = MancalaModel.GOAL_TEST(state1)
#         info = {}

#         # display support
#         if self.render_mode == "human":
#             self.render()
#         return observation, reward, terminated, False, info

#     def render(self):
#         # if self.render_mode is None:
#         #     assert self.spec is not None
#         #     gym.logger.warn(
#         #         "You are calling render method without specifying any render mode. "
#         #         "You can specify the render_mode at initialization, "
#         #         f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
#         #     )
#         #     return

#         if self.render_mode == "ansi" or self.render_mode is None:
#             return self._render_text()
#         # else:
#         #     return self._render_gui(self.render_mode)

#     def _render_text(self):
#         return str(self.state)

#     # def _render_gui(self, mode):
#     #     if self.window_surface is None:
#     #         pygame.init()

#     #         if mode == "human":
#     #             pygame.display.init()
#     #             pygame.display.set_caption("Uniform Coins")
#     #             self.window_surface = pygame.display.set_mode(self.window_size)
#     #         else:  # rgb_array
#     #             self.window_surface = pygame.Surface(self.window_size)
#     #     if self.clock is None:
#     #         self.clock = pygame.time.Clock()

#     #     rect = pygame.Rect((0,0), self.window_size)
#     #     pygame.draw.rect(self.window_surface, self.background_color, rect)
#     #     for coin in range(self.coin_count):
#     #         x = (coin+0.5)*self.cell_size[0]
#     #         y = 0.5*self.cell_size[1]
#     #         r = 0.4*min(self.cell_size)
#     #         if self.state.coin(coin):
#     #             color = self.tail_color
#     #         else:
#     #             color = self.head_color
#     #         pygame.draw.circle(self.window_surface, color, (x,y), r)

#     #     if mode == "human":
#     #         pygame.event.pump()
#     #         pygame.display.update()
#     #         self.clock.tick(self.metadata["render_fps"])
#     #     else:  # rgb_array
#     #         return np.transpose(
#     #             np.array(pygame.surfarray.pixels3d(self.window_surface)), axes=(1, 0, 2)
#     #         )
    
#     def close(self):
#         if self.window_surface is not None:
#             pygame.display.quit()
#             pygame.quit()
#         return
    


    
