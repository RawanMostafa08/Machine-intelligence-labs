from typing import Any, Dict, List


def histogram(values: List[Any]) -> Dict[Any, int]:
    '''
    This function takes a list of values and returns a dictionary that contains the list elements alongside their frequency
    For example, if the values are [3,5,3] then the result should be {3:2, 5:1} since 3 appears twice while 5 appears once 
    '''
    #TODO: ADD YOUR CODE HERE
    Dict = {}
    for value in values:
        Dict[value] = Dict.get(value, 0) + 1
    return Dict