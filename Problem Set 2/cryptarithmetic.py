from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint
from itertools import product

#TODO (Optional): Import any builtin library or define any helper function you want to use

# Var1 can't be equal to var2
def not_equal(var1, var2) -> bool:
    return var1 != var2

# The following functions are used for variable combining
def first_index(var1,var2) -> bool: # ensures that var2 is the first index in the combined var1
    return var1[0] == var2

def second_index(var1,var2) -> bool: # ensures that var2 is the second index in the combined var1
    return var1[1] == var2

def third_index(var1,var2) -> bool: # ensures that var2 is the third index in the combined var1
    return var1[2] == var2

# Makes the summation condition that lhs0 + lhs1 + c_in = rhs + 10 * c_out
def summation_condition(var1,var2) -> bool: 
    return var1[0] + var1[1] + var1[2] == var2[0]+ 10 * var2[1]


# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).

        problem.variables = []
        problem.domains = {}
        problem.constraints = []

        # Reversing the strings to start the addition from the right
        LHS0_reversed = LHS0[::-1] # O W T 
        LHS1_reversed = LHS1[::-1] # O W T   
        RHS_reversed = RHS[::-1]   # R U O F


        variable_set = set() # Make variables_set to prevent duplicates
        letters_set = set()  # Make letters_set to prevent duplicates, this will be used when we don't want to process carries 

        # Add LHS0 characters to variables_set and letters_set
        for char in LHS0_reversed:
            variable_set.add(char)
            letters_set.add(char)

        # Add LHS1 characters to variables_set and letters_set
        for char in LHS1_reversed:
            variable_set.add(char)
            letters_set.add(char)

        # Add RHS characters to variables_set and letters_set
        for char in RHS_reversed:
            variable_set.add(char)
            letters_set.add(char)

        # Adding the domains of the letters as (0,9) unless thet're the last letters then they will be (1,9)
        for letter in list(letters_set):
            if letter == LHS0[0] or letter == LHS1[0] or letter == RHS[0]:
                problem.domains[letter] = set(range(1,10))
            else:
                problem.domains[letter] = set(range(10))

        carries=[]
        # Adding carry variables to variable_set and carries list

        # Unrolling the first carry (dummy carry) with 0 domain
        variable_set.add("C0")
        carries.append("C0")
        problem.domains["C0"] = set(range(0,1)) # 0

        # Looping on carries in the middle and add them to to variable_set and carries list, adding their domains as 0 or 1
        for i in range(1,len(RHS)):
            var = f"C{i}"
            variable_set.add(var)
            carries.append(var)
            problem.domains[var] = set(range(0,2))

        # Unrolling the last carry (dummy carry) with 0 domain
        variable_set.add(f"C{len(RHS)}")
        carries.append(f"C{len(RHS)}")
        problem.domains[f"C{len(RHS)}"] = set(range(0,1)) # 0

        # Padding the LHS0 and LHS1 with dummy variable $ (domain = 0) to be the same size as RHS
        for i in range(0,len(RHS)-len(LHS0)):
            LHS0_reversed += "$" #OWT$
        for i in range(0,len(RHS)-len(LHS1)):
            LHS1_reversed += "$" #OWT$
 
        # Adding the $ to the variable_set and setting its domain to 0
        variable_set.add("$")
        problem.domains["$"] = set(range(0,1)) # 0

        # Converting the set of variables to a list and assigning it to problem.variables
        problem.variables = list(variable_set)

        # Adding the binary constraint so that variable1 can't be equal to variable2
        letters_list=list(letters_set)
        for i in range(0,len(letters_list)):
            for j in range(i + 1 ,len(letters_list)):
                problem.constraints.append(BinaryConstraint((letters_list[i],letters_list[j]),not_equal))


        # C3 C2 C1 C0
        # $  T  W  O
        # $  T  W  O
        # F  O  U  R

        # O + O + C0 = R + 10*C1
        # W + W + C1 = U + 10*C2
        # T + T + C2 = O + 10*C3
        # $ + $ + C3 = F + 10*C4

        # Understanding:
        # For example: A + B = C ternary constraint we should convert to binary
        # (AB)--A : A is the 1st index
        # (AB)--B : B is the 2nd index
        # (AB)--C : first index + 2nd = C

        # This loop adds these remaining constraints as stated in the above example
        for i, _ in enumerate(RHS_reversed):
            lhs0 = LHS0_reversed[i]
            lhs1 = LHS1_reversed[i]
            rhs = RHS_reversed[i]
            carry_in = carries[i] # carry in starting from c0 to c3
            carry_out = carries[i + 1] # carry out starting from c1 to c4


            # Group LHS into one variable and check on the index ordering
            problem.constraints.append(BinaryConstraint(((lhs0,lhs1,carry_in),lhs0),first_index))
            problem.constraints.append(BinaryConstraint(((lhs0,lhs1,carry_in),lhs1),second_index))
            problem.constraints.append(BinaryConstraint(((lhs0,lhs1,carry_in),carry_in),third_index))
            # Add the combined variable to the list of variables, and set its domain to be the cartesian product of its member variable domains
            problem.variables.append((lhs0,lhs1,carry_in))
            merged_domain = list(product(problem.domains[lhs0], problem.domains[lhs1], problem.domains[carry_in]))
            problem.domains[(lhs0, lhs1, carry_in)] = merged_domain


            # Group RHS into one variable and check on the index ordering
            problem.constraints.append(BinaryConstraint(((rhs,carry_out),rhs),first_index))
            problem.constraints.append(BinaryConstraint(((rhs,carry_out),carry_out),second_index))
            # Add the combined variable to the list of variables, and set its domain to be the cartesian product of its member variable domains
            problem.variables.append((rhs,carry_out))
            merged_domain = list(product(problem.domains[rhs], problem.domains[carry_out]))
            problem.domains[(rhs,carry_out)] = merged_domain


            # Check that these two combined variables (lhs0,lhs1,carry_in) and (rhs,carry_out) satistfies the summation_condition
            problem.constraints.append(BinaryConstraint(((lhs0,lhs1,carry_in),(rhs,carry_out)),summation_condition))
            # Add the combined variable to the list of variables, and set its domain to be the cartesian product of its member variable domains
            problem.variables.append((lhs0,lhs1,carry_in))
            merged_domain = list(product(problem.domains[lhs0], problem.domains[lhs1],problem.domains[carry_in]))
            problem.domains[(lhs0,lhs1,carry_in)] = merged_domain

            problem.variables.append((rhs,carry_out))
            merged_domain = list(product(problem.domains[rhs], problem.domains[carry_out]))
            problem.domains[(rhs,carry_out)] = merged_domain


        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())