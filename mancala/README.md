## Mancala Environment

# Description

mancala_v1 is implements the two player board game utilizing a pettingzoo environment. Players take turns picking up and moving pieces to try and store more points than their opponent.

# Observation Space

A 1x14 numpy array that starts with the first players pits (6) and store, followed by the second players pits (6) and store.

# Action Space

An integer of the 0-5 index on the current players side.

# Starting State

All pits have 4 stones, and each store is empty.

# Rewards

3 points for each stone in the players store and 1 point for each stone in a players pit, minus 3 points for each stone in the opposing players store and 1 point for each stone in a players pit.
