from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils

#TODO: Import any modules you want to use
from queue import PriorityQueue

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

# This function checks if the element is found in the fronteir queue or not for a normal deque
def in_queue_fronteir(fronteir: deque,child: S):
    for element,_ in fronteir: # Loops over the fronteir elements to check if the child is present
        if element == child:
            return True
    return False

# This function checks if the element is found in the fronteir queue or not for a priority queue of tuple length = 4
def in_pqueue_fronteir(fronteir: PriorityQueue,child: S):
    for _,_,element,_ in fronteir.queue: 
        if element == child:
            return True
    return False

# This function checks if the element is found in the fronteir queue or not for a priority queue of tuple length = 5
def in_pqueue_Astar_fronteir(fronteir: PriorityQueue,child: S):
    for _,_,_,element,_ in fronteir.queue: 
        if element == child:
            return True
    return False


def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE

    if problem.is_goal(initial_state): # Check if the initial state is actually the goal
        return [] # Then return empty list (no steps needed, we're already at the goal)
    
    fronteir = deque([(initial_state,[])]) # Initialize the fronteir as FIFO queue of tuple (state,path from the parent to reach this state)
    explored = set() # Initialize the explored set
    while fronteir: # While fronteir not empty
        node,path = fronteir.popleft() # Pop the first entered element (leftmost) to treat the deque as a FIFO queue
        explored.add(node) # Add to explored set

        for action in problem.get_actions(node):   # Loop on possible actions from this node
            child = problem.get_successor(node,action)  # Apply this action and get its result node (child)
            if child not in explored and not in_queue_fronteir(fronteir,child): # If the child is not in explored set 
                                                                                  # and not in the fronteir

                if problem.is_goal(child): # If it's the goal             
                    return path+[action]   # return the path of this child plus the last action that got us to the goal
                fronteir.append((child,path+[action])) # if not the goal, add to fronteir
    return None # if fronteir is empty, this means that all nodes are searched and goal is not found


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    fronteir = deque([(initial_state, [])])  # Initialize the fronteir as LIFO stack of tuple (state,path from the parent to reach this state)
    explored = set() # Initialize the explored set
    while fronteir: # While fronteir not empty
        node,path = fronteir.pop() # Pop the last entered element (rightmost) to treat the deque as a LIFO stack

        if problem.is_goal(node):  # Check if the state is the goal
            return path # then return the path from the parent to this node
        
        if node not in explored:
            explored.add(node) # Add to explored set
            for action in problem.get_actions(node): # Loop on possible actions from this node
                child = problem.get_successor(node, action) # Apply this action and get its result node (child)

                if child not in explored and not in_queue_fronteir(fronteir,child):# If the child is not in explored set 
                                                                                  # and not in the fronteir
                    fronteir.append((child, path + [action])) # Append to fronteir with the path= path + last action


def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:

    fronteir = PriorityQueue() # Initialize the fronteir as a priority queue
    x = 0 
    fronteir.put((0, x, initial_state, []))  # Tuple (priority-->cost, index, state, path from the parent to reach this state)
                                             # The index is the order of entrance, it's added to solve the ambiguity in case the priorities are equal
    explored = {}  # explored dictionary {state:cost}

    while not fronteir.empty():
        cost, _, node, path = fronteir.get()  # Pop the node with the least cost

        if problem.is_goal(node): # If it's the goal             
            return path # return the path from the parent to this node
        
        if node not in explored or explored[node] > cost: 
            explored[node] = cost   # Add the node to explored if it's not explored or it's old cost is larger than current cost 

        for action in problem.get_actions(node): # Loop on all possible actions
            child = problem.get_successor(node, action)  # Apply this action and get its result node (child)

            new_cost = cost + problem.get_cost(node, action) # calculate the new cost to be old cost + the cost to apply this action

            if child not in explored and not in_pqueue_fronteir(fronteir,child): # If the child is not in explored dict 
                                                                                  # and not in the fronteir
                fronteir.put((new_cost, x, child, path + [action])) # add to fronteir 
                explored[child] = new_cost  # add child to explored dict
                x += 1  # increment the index of entrance

            elif in_pqueue_fronteir(fronteir,child): # If it's already in the fronteir
                    for got_cost,got_x,element,got_path in fronteir.queue:  
                        if element == child and got_cost > new_cost: # check if it exists with a cost larger than the new cost, then replace the existing one with the new
                            fronteir.queue.remove((got_cost,got_x,element,got_path)) # remove existing
                            fronteir.put((new_cost, x, child, path + [action])) # add the new
                            x += 1   # increment the index of entrance
    return None 


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    fronteir = PriorityQueue() # Initialize the fronteir as a priority queue
    x = 0
    fronteir.put((heuristic(problem,initial_state),0, x, initial_state, []))   # Tuple (priority--> heuristic + path cost to reach this state , index, state, path from the parent to reach this state)
                                                                          # The index is the order of entrance, it's added to solve the ambiguity in case the priorities are equal
    explored = {}  # explored dictionary {state:g(n)}


    while not fronteir.empty():
        f,g, _, node, path = fronteir.get()   # Pop the node with the least f(n)

        if problem.is_goal(node):# If it's the goal    
            return path # return the path from the parent to this node
        
        if node not in explored or explored[node] > g:
            explored[node] = g  # Add the node to explored if it's not explored or it's old g(n) is larger than current g(n) 

        for action in problem.get_actions(node):  # Loop on all possible actions
            child = problem.get_successor(node, action)  # Apply this action and get its result node (child)

            new_cost = g + problem.get_cost(node, action) # calculate the new cost to be old cost + the cost to apply this action

            if child not in explored and not in_pqueue_Astar_fronteir(fronteir,child): # If the child is not in explored dict 
                                                                                  # and not in the fronteir
                f_cost = new_cost + heuristic(problem, child) # calculate the f(n) = g(n) + h(n)
                fronteir.put((f_cost,new_cost, x, child, path + [action])) # add to fronteir 
                explored[child] = new_cost # add child to explored dict
                x += 1  # increment the index of entrance
    return None 


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    fronteir = PriorityQueue() # Initialize the fronteir as a priority queue
    x = 0
    fronteir.put((heuristic(problem,initial_state), x, initial_state, []))  # Tuple (priority-->heuristic, index, state, path from the parent to reach this state)
                                                                          # The index is the order of entrance, it's added to solve the ambiguity in case the priorities are equal
    explored = {}  # explored dictionary {state:heuristic}

    while not fronteir.empty(): 
        h, _, node, path = fronteir.get()   # Pop the node with the least heuristic

        if problem.is_goal(node): # If it's the goal    
            return path # return the path from the parent to this node
        
        if node not in explored or explored[node] > h:
            explored[node] = h  # Add the node to explored if it's not explored or it's old heuristic is larger than current heuristic 

        for action in problem.get_actions(node): # Loop on all possible actions
            child = problem.get_successor(node, action) # Apply this action and get its result node (child)

            if child not in explored and not in_pqueue_fronteir(fronteir,child):  # If the child is not in explored dict 
                                                                                  # and not in the fronteir
                fronteir.put((heuristic(problem,child), x, child, path + [action]))  # add to fronteir 
                explored[child] = h   # add child to explored dict
                x += 1  # increment the index of entrance
    return None 