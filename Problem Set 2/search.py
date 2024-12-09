from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented
from typing import Optional


#TODO: Import any built in modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # This function is the recursive version of minimax
    def minimax_value(state: S, depth: int) -> Tuple[float, Optional[A]]:
        # Terminal test: if the state is terminal, then return values[0] because game.is_terminal(s) returns the values
        # for all the agents. So to get the value for the player (which acts at the max nodes) we use values[0]
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None # No action at terminal state
        
        # If max depth is reached, return the heuristic about the utility at this state
        if max_depth != -1 and depth == max_depth:
            return heuristic(game, state, 0), None 
        
        # Maximize if it's the player's turn, anyone else minimize
        if game.get_turn(state) == 0:  
            return max_value(state, depth)
        else:
            return min_value(state, depth)


    def max_value(state: S, depth: int) -> Tuple[float, Optional[A]]:
        # start max_value with -infinity
        max_v = float('-inf')
        best_action = None
        for action in game.get_actions(state): # Loop on all possible actions
            successor = game.get_successor(state, action) # Get the successor of this action
            value, _ = minimax_value(successor, depth + 1) # Recurse passing the new successor and incrementing the depth

            # Update max_v if the returned value is strictly larger, update the action as best_action
            if value > max_v: 
                max_v = value
                best_action = action
        return max_v, best_action

    def min_value(state: S, depth: int) -> Tuple[float, Optional[A]]:
        # start max_value with infinity
        min_v = float('inf')
        best_action = None
        for action in game.get_actions(state): # Loop on all possible actions
            successor = game.get_successor(state, action) # Get the successor of this action
            value, _ = minimax_value(successor, depth + 1) # Recurse passing the new successor and incrementing the depth

            # Update min_v if the returned value is strictly smaller, update the action as best_action
            if value < min_v:
                min_v = value
                best_action = action
        return min_v, best_action

    # Call the recursive function with 0 initial depth
    return minimax_value(state, 0)

    
# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # This function is the recursive version of alphabeta pruning
    def aphabeta_value(state: S, depth: int, alpha, beta) -> Tuple[float, Optional[A]]:
        # Terminal test: if the state is terminal, then return values[0] because game.is_terminal(s) returns the values
        # for all the agents. So to get the value for the player (which acts at the max nodes) we use values[0]
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None  # No action at terminal state
        
        # If max depth is reached, return the heuristic about the utility at this state
        if max_depth != -1 and depth == max_depth:
            return heuristic(game, state, 0), None 
        
        # Maximize if it's the player's turn, anyone else minimize
        if game.get_turn(state) == 0:  
            return max_value(state, depth, alpha, beta)
        else:
            return min_value(state, depth, alpha, beta)

    def max_value(state: S, depth: int, alpha, beta) -> Tuple[float, Optional[A]]:
        # start max_value with -infinity
        max_v = float('-inf')
        best_action = None
        for action in game.get_actions(state): # Loop on all possible actions
            successor = game.get_successor(state, action) # Get the successor of this action
            value, _ = aphabeta_value(successor, depth + 1, alpha, beta) # Recurse passing the new successor and incrementing the depth

            # Update max_v if the returned value is strictly larger, update the action as best_action
            if value > max_v:
                max_v = value
                best_action = action

            # If max_v is greater than or equal to beta--> prune the remaining branches
            # This branch cannot influence the decision of the parent node
            if max_v >= beta:
                return max_v,best_action
            # Update alpha to be the maximum of previous alpha and max_v
            alpha = max(alpha,max_v)

        return max_v, best_action

    def min_value(state: S, depth: int, alpha, beta) -> Tuple[float, Optional[A]]:
        # start max_value with infinity
        min_v = float('inf')
        best_action = None
        for action in game.get_actions(state): # Loop on all possible actions
            successor = game.get_successor(state, action) # Get the successor of this action
            value, _ = aphabeta_value(successor, depth + 1, alpha, beta)  # Recurse passing the new successor and incrementing the depth

            # Update min_v if the returned value is strictly smaller, update the action as best_action
            if value < min_v:
                min_v = value
                best_action = action

            # If min_v is smaller than or equal to alpha --> prune the remaining branches
            # This branch cannot influence the decision of the parent node
            if min_v <= alpha:
                return min_v,best_action
            # Update beta to be the minimum of previous beta and min_v
            beta = min(beta,min_v)

        return min_v, best_action

    # Start the recursion with initial depth =0, alpha = -infinity, beta = infinity
    return aphabeta_value(state = state, depth= 0, alpha = float('-inf'), beta = float('inf'))


# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # This function is the recursive version of alphabeta pruning
    def alphabeta_value(state: S, depth: int, alpha, beta) -> Tuple[float, Optional[A]]:
        # Terminal test: if the state is terminal, then return values[0] because game.is_terminal(s) returns the values
        # for all the agents. So to get the value for the player (which acts at the max nodes) we use values[0]
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None # No action at terminal state
        
        # If max depth is reached, return the heuristic about the utility at this state
        if max_depth != -1 and depth == max_depth:
            return heuristic(game, state, 0), None
        
        # Maximize if it's the player's turn, anyone else minimize
        if game.get_turn(state) == 0: 
            return max_value(state, depth, alpha, beta)
        else: 
            return min_value(state, depth, alpha, beta)

    def max_value(state: S, depth: int, alpha, beta) -> Tuple[float, Optional[A]]:
        # start max_value with -infinity
        max_v = float('-inf')
        best_action = None

        actions = game.get_actions(state)
        # Sort the actions based on the heuristic value of their successors
        # Actions are sorted in descending order for the maximizing player (to prioritize the best moves first)
        # Goal: increasing the chances of pruning earlier by explore the most promising branches first
        actions = sorted(actions, key=lambda a: heuristic(game, game.get_successor(state, a), 0), reverse=True)

        for action in actions: # Loop on all possible actions
            successor = game.get_successor(state, action)  # Get the successor of this action
            value, _ = alphabeta_value(successor, depth + 1, alpha, beta) # Recurse passing the new successor and incrementing the depth

            # Update max_v if the returned value is strictly larger, update the action as best_action
            if value > max_v:
                max_v = value
                best_action = action

            # If max_v is greater than or equal to beta--> prune the remaining branches
            # This branch cannot influence the decision of the parent node
            if max_v >= beta:
                return max_v, best_action
            # Update alpha to be the maximum of previous alpha and max_v
            alpha = max(alpha, max_v)

        return max_v, best_action

    def min_value(state: S, depth: int, alpha, beta) -> Tuple[float, Optional[A]]:
        # start max_value with infinity
        min_v = float('inf')
        best_action = None

        actions = game.get_actions(state)
        # Sort the actions based on the heuristic value of their successors
        # Actions are sorted in ascending order for the minimzing player
        # Goal: increasing the chances of pruning earlier by explore the most promising branches first
        actions = sorted(actions, key=lambda a: heuristic(game, game.get_successor(state, a), 0))

        for action in actions:  # Loop on all possible actions
            successor = game.get_successor(state, action)  # Get the successor of this action
            value, _ = alphabeta_value(successor, depth + 1, alpha, beta) # Recurse passing the new successor and incrementing the depth

            # Update min_v if the returned value is strictly smaller, update the action as best_action
            if value < min_v:
                min_v = value
                best_action = action

            # If min_v is smaller than or equal to alpha --> prune the remaining branches
            # This branch cannot influence the decision of the parent node
            if min_v <= alpha:
                return min_v, best_action
            # Update beta to be the minimum of previous beta and min_v
            beta = min(beta, min_v)

        return min_v, best_action
    
    # Start the recursion with initial depth =0, alpha = -infinity, beta = infinity
    return alphabeta_value(state=state, depth= 0, alpha = float('-inf'), beta = float('inf'))


# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # This function is the recursive version of minimax
    def expectimax_value(state: S, depth: int) -> Tuple[float, Optional[A]]:
        # Terminal test: if the state is terminal, then return values[0] because game.is_terminal(s) returns the values
        # for all the agents. So to get the value for the player (which acts at the max nodes) we use values[0]
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None # No action at terminal state
        
        # If max depth is reached, return the heuristic about the utility at this state
        if max_depth != -1 and depth == max_depth:
            return heuristic(game, state, 0), None 
        
        # Maximize if it's the player's turn, anyone else is a probability node
        if game.get_turn(state) == 0:  
            return max_value(state,depth)
        else:
            return chance_value(state,depth)


    def max_value(state: S, depth: int) -> Tuple[float, Optional[A]]:
        # start max_value with -infinity
        max_v = float('-inf')
        best_action = None
        
        for action in game.get_actions(state):  # Loop on all possible actions
            successor = game.get_successor(state, action) # Get the successor of this action
            value, _ = expectimax_value(successor, depth + 1) # Recurse passing the new successor and incrementing the depth

            # Update max_v if the returned value is strictly larger, update the action as best_action
            if value > max_v:
                max_v = value
                best_action = action
        return max_v, best_action
    
    def chance_value(state: S, depth: int) -> Tuple[float, Optional[A]]:

        # If there are no available actions for the current state, return the heuristic value for this state.
        if len(game.get_actions(state)) == 0:
            return heuristic(game,state,0), None
        
        expected = 0

        for action in game.get_actions(state): # Loop on all possible actions

            successor = game.get_successor(state, action) # Get the successor of this action
            value, _ = expectimax_value(successor, depth + 1) # Recurse passing the new successor and incrementing the depth

            # Accumulate the expected value by averaging the values of all possible successor states
            # p = 1 / len(game.get_actions(state))
            expected += value / len(game.get_actions(state))
        
        return expected, None
    
    # Start the recursion with initial depth =0
    return expectimax_value(state, 0)
