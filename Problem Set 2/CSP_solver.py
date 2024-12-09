from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    # Do forward checking on all of the problem constraints
    for constraint in problem.constraints:

        if isinstance(constraint,BinaryConstraint): # if this constraint is a binary constraint
            binary_constraint: BinaryConstraint = constraint # Downcast constraint to BinaryConstraint

            if assigned_variable in binary_constraint.variables: # if the passed assigned_variable is in this constraint
                other_variable = binary_constraint.get_other(assigned_variable) # then get the other variable in the constraint

                if other_variable not in domains: # Make sure that the other variable is in the domains dict (unassigned)
                    continue # Continue if the variable is already assigned

                new_domain = set()  
                for value in domains[other_variable]: 
                    assignment={ assigned_variable : assigned_value, other_variable : value }
                    if binary_constraint.is_satisfied(assignment):
                        # Add the value if it satisfies the constraint with the assigned variable
                        new_domain.add(value) 
                if not new_domain: # If no value satisfies the constraint, return false
                    return False
                
                # Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable
                domains[other_variable] = new_domain

    return True


# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:

    values_counts={} # Dictrinary to keep track of other variabes value counts for each value, i.e {value:values_count}
    for value in domains[variable_to_assign]: # Try all the values in the variable_to_assign domain
        values_count = 0
        for constraint in problem.constraints:

            if isinstance(constraint,BinaryConstraint): # if this constraint is a binary constraint
                binary_constraint: BinaryConstraint = constraint # Downcast constraint to BinaryConstraint

                if variable_to_assign in binary_constraint.variables:  # if the passed variable_to_assign is in this constraint
                    other_variable = binary_constraint.get_other(variable_to_assign) # then get the other variable in the constraint

                    if other_variable not in domains: # Make sure that the other variable is in the domains dict (unassigned)
                        continue # Continue if the variable is already assigned

                    for other_value in domains[other_variable]:
                        assignment={ variable_to_assign:value, other_variable:other_value }
                        if binary_constraint.is_satisfied(assignment):
                            # increment values_count if it satisfies the constraint with the assigned variable
                            values_count += 1
        values_counts[value] = values_count

    # Sort the values descendingly, values with larger value counts first (meaning they're least restraining) 
    sorted_values = sorted(values_counts.keys(), key=lambda v: (-values_counts[v], v))

    return sorted_values
    

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
#           Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    if not one_consistency(problem): # Check on one consistency, if not satisfied then no solution
        return None
    
    # Call backtrack function that does the recursion logic
    # Taking empty assignemnt, problem, domains
    return backtrack({}, problem, problem.domains) 

def backtrack(assignment: Assignment, problem: Problem, domains) -> Optional[Assignment]:

    if problem.is_complete(assignment): # Base case: if assignment is complete, return it as the solution
        return assignment
    
    # Next variable is the one with MRV
    var = minimum_remaining_values(problem, domains)
    
    # Next value is the one with least restraining values
    for value in least_restraining_values(problem, var, domains):
        assignment[var] = value # Assign this value to the variable "var"(MRV)

        domain_copy = domains.copy() # Take a copy of the domain to avoid editing the problem domain
        domain_copy.pop(var) # Pop the variable being processed
        
        if forward_checking(problem, var, value, domain_copy): 
            # If forward checking passes: recurse with the new assignment and new domain, until complete assignment 
            result = backtrack(assignment, problem, domain_copy)
            
            if result is not None:
                return result
        # Pop the variable from the assignment if forward checking fails
        assignment.pop(var)

    return None
