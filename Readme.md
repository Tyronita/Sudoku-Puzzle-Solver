# Sudoku Solution Readme

This readme documents each component of the solution and how they work together to produce a solution or conclude there is no solution for a given 9x9 puzzle.

---

## Game state methods and modifying the board


### 1. is_solved
    Returns whether the current sudoku board is solved -> every row, column and subgrid should contain the values 1-9 once.

### 2. is_illegal_board
    Returns whether an unfinished sudoku it is an illegal board -> et least one row, column and subgrid should contain the values 1-9 more than once.

---

## The Variables, Domain and Constraints

A `variable` is defined by an empty space, represented by 0, on the suodku board.

A `constraint` is defined by a rule which allows a value to exist at a position in the problem.

A `domain ` is the list of legal values a variable can take according to a constraint.

### 1. get_variables
    Returns a list of the empty spaces (0s) in a given sudoku board.

### 2. insert_value
    Inserts the value of a given variable into the sudoku board at the variable's position.

### 3. satisfies_constraint
    Given a new possible variable value, determine whether this would be a legal value at that position in the board.

### 4. get_domain
    For every variable, returns the list of legal values a variable can take according to a constraint,.

---

## Arc-consistency algorithm


A `neighbour ` of a variable is another variable which is in the same row, column or subgrid as the variable.

An `arc` is a bi-directional connection between two variables.

An arc is `consistent` if the related variables are satisfied by the constraint.

### 1. get_neighbour_nodes
    Given a list of variables -> returns each variable's neighbours (in ths same subgrid, row or column.)

### 2. revise_domain
    Given the index of a variables i and j, remove values from the domain of i which form no relation with the values from the domain of var j. 

### 3. arc_consistency
    Makes arcs between all arcs in the problem consistent by removing all domains of all inconsistent domain values.
    Returns a boolean indicating false if any of these domains are now empty and false if all arcs are consistent.

---

## Backtracking algorithm

### 1. most_constrained_variable
    Picks the variable with the shortest domain.

### 2. backtrack_search
    1. Makes an assignment from the shortest of the arc-consistent domains (most_constrained_variablr). 
    2. It then repeats the AC algorithm until arcs are inconstent or the board is solved.
    3. This process is repeated recursively until the end of the 

---

## Complete solution

### sudoku_solver
    1. Pre-emptively check whether the given board was illegal.
    3. Get the domain and variables of the initial board.
    2. Make arcs consistent.
    3. If domain lengths of all variables are 1 then the probelm is complete, else it starts backtrack_search.
    4. If the solution is complete, it will return it, else if it is unsolvable it will return -1 in the poaition of all entries.

### Pros and cons of solution and choice of algorithm
    Pros:
    - The minimum remaining value / most constrained variable heuristic, fixed in place the shortest domains, which greatly reduced redundant computation.
    - The is_constraint_satisfied action is the most heavily used function and operates very fast due to the use of sets of all other values related to the variable.
    - The backtrack search algorithm makes use of the previously revised domain in its first iteration, this reduces the length of the initial set of domains.

    Cons:
    - A con of my solution is that my backtracking solution ignores the fact that order of assignments commute, so a path can be tried twice, which is redundant computation.
    - Interference / forward checking could be made use of to eliminate paths whose arcs to their neighbours lead to a dead end.
    
## References
    Arc-consistency and backtracking search are based on the psuedo-code in section 6 of Russell and Norvig's 'Artificial Intelligence: A Modern Approach'.
