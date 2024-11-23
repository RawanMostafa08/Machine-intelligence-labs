from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers import utils

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point]
# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE

        return self.cars # Return cars initial state
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #TODO: ADD YOUR CODE HERE

        for car_position, slot_index in self.slots.items(): # Loop on slots which contains the true slots that the cars should be in
            if state[slot_index] != car_position:  # If any car position in the current state doesn't equal its correct position in slots, then it's not goal yet
                return False
        return True # else, it's the goal state, meaning the above condition hasn't been entered any time
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        #TODO: ADD YOUR CODE HERE

        actions = []
        for i, car_position in enumerate(state):
            for direction in Direction: # Try every possible direction
                position = car_position + direction.to_vector() # new car position is old position + the direction vector it will take

                if position not in self.passages or position in set(state): continue # If the position is in state then its occupied slot
                                                                                     # If the position isn't in passages then its not a slot (wall)
                actions.append((i,direction)) # else, append the direction as possible action
        return actions
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE

        car_index, action_dir = action 
        new_car_position = state[car_index] + action_dir.to_vector() # new car position is old position + the direction vector it will take

        new_state=list(state) # Convert the state to list to be mutable
        new_state[car_index]=new_car_position # update the position of the car 
        new_state=tuple(new_state) # Convert back to tuple

        return new_state
    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #TODO: ADD YOUR CODE HERE
        car_index, action_dir = action
        new_car_position = state[car_index] + action_dir.to_vector() # New car position is old position + the direction vector it will take

        if new_car_position in self.slots and self.slots[new_car_position] != car_index: # If the new position is another car's correct position then the cost is 101
            return 101
        else: # else, it's an empty slot that's no one's property, then cost is 1
            return 1
    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
