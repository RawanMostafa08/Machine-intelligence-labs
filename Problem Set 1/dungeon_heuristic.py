from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils

# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)

#TODO: Import any modules and write any functions you want to use

def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    #TODO: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.is_goal" HERE.
    # Calling it here will mess up the tracking of the explored nodes count
    # which is considered the number of is_goal calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
        # Cache to store computed values for performance
    

    if not state.remaining_coins: # If there's no coins left just return the manhattan distance to the exit 
        # This condition is to avoid line 27,30 from throwing an error if state.remaining_coins is empty 
        return manhattan_distance(state.player, problem.layout.exit)
    
    # Loop on all remaining coins to get the one with the min manhattan distance from the player
    nearest_coin_distance = min(manhattan_distance(state.player, coin) for coin in state.remaining_coins) 
    
    # Loop on all remaining coins to get the one with the min manhattan distance from the exit
    exit_distance = min(manhattan_distance(coin, problem.layout.exit) for coin in state.remaining_coins)
    
    # Set the heuristic value to be ( distance from the player to its nearest coin ) + ( distance from the exit to its nearest coin ) 
    return nearest_coin_distance  + exit_distance
    