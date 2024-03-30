import numpy as np
import copy

class MancalaState:
    """A collection of N coins. Turn over coins until all coins are tails, or all coins are heads."""

    def __init__(self, size=6):
        sz = size * 2 + 2
        self._pits = np.zeros(sz, dtype=np.int8)
        self._size = sz
        # 1 is player 1 and 2 is player 2
        self._turn = 1
        self._winner = None
        return
    
    @property
    def winner(self):
        if self._winner == None:
            return None
        elif self._winner == 1:
            return 0
        elif self._winner == 2:
            return 1
        elif self._winner == 0:
            return -1

    @property
    def turn(self):
        return self._turn
    
    @turn.setter
    def turn(self, new_turn):
        self._turn = new_turn

    @property
    def size(self):
        return self._size

    def randomize(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
        stones = (self._size - 2) * 4
        while stones > 0:
            rand_pit = np.random.randint(0,self._size)
            rand_stone_count = np.random.randint(1,stones+1)
            stones -= rand_stone_count
            self._pits[rand_pit] += rand_stone_count
        return self._pits
    
    def reset(self):
        for i in range(self._size-1):
            if i == self._size // 2 - 1:
                self._pits[i] = 0
                continue
            self._pits[i] = 4
        self._pits[self._size-1] = 0 
        self._turn = 1
        self._winner = None

    # To do: add repeat turn 
    def empty_pit(self, action):
        """action: integer index into _pits"""
        # Make basic movement
        if self._turn == 2:
            action += self._size // 2 
        stones = self._pits[action]
        self._pits[action] = 0
        current_pit = action + 1
        while stones > 0:
            if current_pit == self._size // 2 - 1 and self._turn == 2:
                current_pit += 1

            self._pits[current_pit] += 1
            current_pit += 1
            stones -= 1
            if current_pit >= self._size or (current_pit == self._size - 1 and self._turn == 1):
                current_pit = 0

        if current_pit != 0 and current_pit != self._size // 2:
            current_pit -= 1
            if self._pits[current_pit] == 1:
                if (self._turn == 1 and current_pit < self._size // 2 - 1 and self._pits[current_pit + (2*((self._size // 2) - 1 - current_pit))] > 0):
                    self._pits[self._size // 2 - 1] += self._pits[current_pit]
                    self._pits[current_pit] = 0
                    other_pit = current_pit + (2*((self._size // 2) - 1 - current_pit))
                    self._pits[self._size // 2 - 1] += self._pits[other_pit]
                    self._pits[other_pit] = 0
                elif (self._turn == 2 and current_pit > self._size // 2 - 1 and self._pits[current_pit-(2*(current_pit-(self._size//2)+1))] > 0):
                    self._pits[self._size - 1] += self._pits[current_pit]
                    self._pits[current_pit] = 0
                    other_pit = current_pit-(2*(current_pit-(self._size//2)+1))
                    self._pits[self._size - 1] += self._pits[other_pit]
                    self._pits[other_pit] = 0
        elif (current_pit == 0 and self._turn == 2) or (current_pit == self._size // 2 and self._turn == 1):
            self.swap_turns()

        # Check if one row is empty to end game
        found_filled_pit = False
        for i in range(self._size-1):
            if i == self._size // 2 - 1:
                if found_filled_pit == False:
                    break
                found_filled_pit = False
                continue
            if self._pits[i] > 0:
                found_filled_pit = True
        
        self.swap_turns()

        # If a pit is found to be filled, then return
        if found_filled_pit == True: 
            return

        # Sum up remaining stones in each row
        self._pits[self._size // 2 - 1] += sum(self._pits[:self._size//2-1])
        self._pits[self._size-1] += sum(self._pits[self._size // 2:self._size-1])

        # Empty the rows
        for i in range(self._size-1):
            if i == self._size // 2 - 1:
                continue
            self._pits[i] = 0
        self._turn = None
        return
    
    def game_over(self):
        if self._turn == None:
            if self._pits[self._size // 2 - 1] == self._pits[self._size-1]:
                self._winner = 0
            elif self._pits[self._size // 2 - 1] > self._pits[self._size-1]:
                self._winner = 1
            else:
                self._winner = 2
            return True
        return False

    @property
    def observation(self):
        return self._pits

    @observation.setter
    def observation(self, new_board):
        print(new_board)
        for ind, elt in enumerate(new_board):
            self._pits[ind] = elt
        return

    def pit(self, index):
        return self._pits[index]
    
    def swap_turns(self):
        if self._turn == 1:
            self._turn = 2
        else:
            self._turn = 1

    def reward(self):
        return (self._pits[self._size // 2 - 1] - self._pits[self._size-1], self._pits[self._size-1] - self._pits[self._size // 2 - 1])

    def __str__(self):
        s = "|"
        top = self._pits[self._size//2:]
        top = np.flip(copy.deepcopy(top))
        for pit in top:
            s += f" {pit:{2}d} |"
        s += f"    |\n|    |"
        bottom = self._pits[:self._size//2]
        for pit in bottom:
            s += f" {pit:{2}d} |"
        s += "\n\n\n"
        return s

if __name__ == "__main__":
    s = MancalaState(6)
    # print(s)
    # s.randomize()
    # print(s)
    # s.randomize()
    # print(s)
    # s.reset()
    # print("This is the start \n\n")
    # print(s.observation)
    # print(s)
    # while s.turn != None:
    #     s.empty_pit(int(input(f"Turn {s.turn} Enter a pit to empty:")))
    #     print(s)

    
class MancalaModel:

    def ACTIONS(state):
        actions = []
        player = state.turn
        for i in range(state.size // 2 - 1):
            if player == 2:
                ind = i + (state.size // 2)
            else:
                ind = i
            if state.observation[ind] > 0:
                actions.append(i)
        return actions

    def RESULT(state, action):
        state1 = copy.deepcopy(state)
        state1.empty_pit(action)
        return state1

    def GOAL_TEST(state):
        for i in range(state.size-1):
            if i == state.size // 2 - 1:
                continue
            if state.pits[i] != 0:
                return False
        return True

    def STEP_COST(state, action, state1):
        return 1

    def HEURISTIC(state):
        estimated_cost = 0.0
        return estimated_cost
    
    def STRINGIFY_STATE(state):
        retString = ""
        for i in state.observation:
            retString += f"{i:0{2}d}"
        # print(retString)
        retString += f"{state.turn}"
        return retString

# if __name__ == "__main__":
#     state = UniformCoinsState(7)
#     state.randomize()
#     actions = UniformCoinsModel.ACTIONS(state)
#     print(actions)

#     state = UniformCoinsState(13)
#     state.randomize()
#     actions = UniformCoinsModel.ACTIONS(state)
#     print(actions)

#     print()
#     state = UniformCoinsState(13)
#     state.randomize()
#     print(state)
#     state1 = UniformCoinsModel.RESULT(state, 4)
#     print(state1)

#     print()
#     state = UniformCoinsState(13)
#     print(UniformCoinsModel.GOAL_TEST(state))
#     state.randomize()
#     print(UniformCoinsModel.GOAL_TEST(state))
    
#     print()
#     state = UniformCoinsState(13)
#     state.randomize()
#     print(state)
#     action = 2
#     state1 = UniformCoinsModel.RESULT(state, action)
#     print(UniformCoinsModel.STEP_COST(state, action, state1))

    
