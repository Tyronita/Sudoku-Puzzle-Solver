import numpy as np, math
from data_structures import Queue


def get_variables(sudoku: object) -> list:
    """
    Returns a list of the empty spaces (0s) in a given sudoku board.
    Input
        sudoku: 9x9 numpy array
            Empty cells are designated by 0.

    Output
        variables:
            list of tuples of length 2. Each tuple containing the position (row, col) of variables in the sudoku board.
            
    """
    # Initialise variables: each var will be the position of an empty space. Denoted by 0. 
    variables = []

    # 9 x 9 sudoku board = 81 iterations
    for row_idx in range(9): 
        for col_idx in range(9):

            if sudoku[row_idx][col_idx] == 0:
                # Position is stored in the form of a tuple (row, column) / matrix notation
                postion = (row_idx, col_idx)
                variables.append(postion)

    return variables



def get_domains(sudoku: object, variables: list) -> list or None:
        """
        Returns the list of legal values a variable can take according to a constraint, for every variable.

        Input
            sudoku: 9x9 numpy array
                Empty cells are designated by 0.
            variables:
                list of tuples of length 2. Each tuple containing the position (row, col) of variables in the sudoku board.

        Output
            domain: dictionary of lists
                Each nested list contains the legal values that a variable can take.
        """

        domains = dict()

        # Extract row and column of variable
        for var_i in variables:

            # Extract rows and columns
            row_idx, col_idx = var_i
            row, column = list(sudoku[row_idx]), list(sudoku[:,col_idx])

            # Extract the rows of the subgrid
            start_subgrid_row_idx = 3 * (row_idx // 3)
            subgrid = sudoku[start_subgrid_row_idx : start_subgrid_row_idx + 3]

            # Extract the columns of the subgrid
            start_subgrid_col_idx = 3 * (col_idx // 3)
            subgrid = list(subgrid[:, start_subgrid_col_idx : start_subgrid_col_idx + 3].flatten())

            # If any values repeat then -> not valid
            possible_values = set(list(range(1, 10)))
            existing_values = set(row + column + subgrid)
            
            domains[var_i] = list(possible_values.difference(existing_values))

        # if not update operation -> return new copy
        return domains



def insert_value(sudoku: object, variable: tuple, value: int, return_copy: bool = False) -> None or object:
    """
    Inserts the value of a variable into the sudoku board at the variables position.

    Input
        sudoku: 9x9 numpy array
            Empty cells are designated by 0.

        variable: tuple of length 2
            (rowIdx, colIdx) of the variable's position in the board.

        value: int
            value is between 0-9

        return_copy: bool
            false (default) if this change should be written to the current board. 
            
    Output
        object | none:
            returns 9x9 numpy array if return_copy = true.
    """

    # get row and column for insertion
    row_idx, col_idx = variable

    # return a copy of the board
    if return_copy:
        new_board = np.copy(sudoku)
        new_board[row_idx][col_idx] = value
        return new_board
        
    # or insert by reference
    else:
        sudoku[row_idx][col_idx] = value



def any_duplicates(a_array: object) -> bool:
    """
    Given a 1d numpy array of integers, return whether there is a repeated value that isn't zero.
    """
    # set of already added numbers
    seen = set()
    
    for element in list(a_array):

        # if element is duplicate and is between 1-9 (not 0)
        if element in seen and element != 0:
            return True

        seen.add(element)
        
    return False



def is_illegal_board(sudoku: object) -> bool:
    """
    Takes an unfinished board and determines whether it is an illegal board.

    Input
        sudoku: 9x9 numpy array
            Empty cells are designated by 0.
            
    Ouput
        boolean:
            indicates whether current sudoku board is illegal.
    """
    for i in range(9):

        # 1 & 2. if 1-9 is repeated in rows or column -> illegal
        row = sudoku[i]
        column = sudoku[:,i]
        if any_duplicates(row[row != 0]) or any_duplicates(column[column != 0]):
            return True

    for rowIdx in range(0,9,3):
        for colIdx in range(0,9,3):

            # 3. if 1-9 is repeated in subgrid -> illegal
            subgrid = sudoku[rowIdx: rowIdx + 3][:, colIdx: colIdx + 3].flatten()
            if any_duplicates(subgrid[subgrid != 0]):
                return True
    
    # else: valid
    return False



def satisfies_constraint(sudoku: object, variable: tuple, value: int) -> bool:
    """
    Given a new possible variable value, determine whether this would be a legal move.

    Input
        sudoku: 9x9 numpy array
            Empty cells are designated by 0.

        variable:
            tuple containing the position of the variable (row_idx, col_idx).
            
        value:
            value we're testing is allowed to be at this position

    Output
        boolean:
            indicating whether the value is legal at that position.
    """
    row_idx, col_idx = variable

    # Extract row and column of variable
    row, column = list(sudoku[row_idx]), list(sudoku[:,col_idx])

    # Extract the rows of the subgrid
    start_subgrid_row_idx = 3 * (row_idx // 3)
    subgrid = sudoku[start_subgrid_row_idx : start_subgrid_row_idx + 3]

    # Extract the columns of the subgrid
    start_subgrid_col_idx = 3 * (col_idx // 3)
    subgrid = list(subgrid[:, start_subgrid_col_idx : start_subgrid_col_idx + 3].flatten())

    # If any values repeat then -> not valid
    if value in set(row + column + subgrid):
        return False
    else:
        return True



def revise_domain(sudoku: object, domains: dict, var_i: int, var_j: int) -> bool:
    """
    Given the index of a variables i and j, remove values from the domain of i which form no relation
     with the values from the domain of var j. 

    Input:
        sudoku: 9x9 numpy array
            Empty cells are designated by 0.

        var_i_idx, var_j_idx: positive integer including 0.
            var_i's domain is what we are revising against var_j's domain
        
        domains: list of lists.
            Each sublist contains the allowable values for a variable. var_i_idx = dom_of_var_i_idx.
    
    Output:
        revised: boolean indicating whether the domain has been revised.
        * changes to domain are acheived by reference to the domain argument.
    """

    # flag indicating revision
    revised = False

    # 1. Repeat for every value in the domain of var i
    for var_i_domain_val in list(domains[var_i]):
        
        # Insert var i domain value into copy of board
        new_board = insert_value(sudoku, var_i, var_i_domain_val, True)

        # 2. Create a list of bools for which the domain values of vars i and j satisfy the binary constraint.
        domain_ij_formed_relation = map(lambda var_j_domain_val:
            satisfies_constraint(new_board, var_j, var_j_domain_val), domains[var_j]
        )

        # 3. If no value of domain var j worked for a value of var i -> remove the value from domain of var i
        if not any(domain_ij_formed_relation):
            domains[var_i].remove(var_i_domain_val)
            revised = True     
    
    return revised



def get_neighbour_nodes(variables: list) -> list:
    """
    Given a list of variables -> returns each variable's neighbours.
     
    Input:
        variables:
            list of tuples of length 2. Each tuple containing the position (row, col) of variables in the sudoku board.

    Output:
        neighbours:
            list of sets for each variable containing the indices of the neighbours for the variable.
            var_i_idx = var_i_neighbours_idx
    """
    neighbours = dict()
    for var_i in variables:

        # variable's neighbours is stored in a set
        var_i_neighbours = set()
        for var_j in variables:

            # node cannot be a neighbour of itself
            if var_i != var_j:
                
                # get rows and columns
                var_i_row, var_i_col = var_i 
                var_j_row, var_j_col = var_j

                # 1. If variables in same row -> they are related.
                if var_i_row == var_j_row:
                    var_i_neighbours.add(var_j)
                    continue 

                # 2. If variables in same column -> they are related.
                if var_i_col == var_j_col:
                    var_i_neighbours.add(var_j)
                    continue

                # Determine the subgrid position of i
                var_i_subgrid_row_idx = math.ceil( (var_i_row + 1) / 3) - 1
                var_i_subgrid_col_idx = math.ceil( (var_i_col + 1) / 3) - 1
                var_i_subgrid = (var_i_subgrid_row_idx, var_i_subgrid_col_idx)

                # ... and j
                var_j_subgrid_row_idx = math.ceil( (var_j_row + 1) / 3) - 1
                var_j_subgrid_col_idx = math.ceil( (var_j_col + 1) / 3) - 1
                var_j_subgrid = (var_j_subgrid_row_idx, var_j_subgrid_col_idx)

                # 3. If variables in same subgrid -> they are related.
                if var_i_subgrid == var_j_subgrid:
                    var_i_neighbours.add(var_j)
                    continue

        neighbours[var_i] = var_i_neighbours

    return neighbours



def arc_consistency(sudoku: object, variables: list, domains: dict) -> bool:
    """
    Makes arcs between all arcs in the problem consistent by removing all domains of all inconsistent domain values.
    Returns a boolean indicating false if any of these domains are now empty.
    Input
        sudoku: 9x9 numpy array
            Empty cells are designated by 0.

        variables: list of tuples of length 2.
            Each tuple containing the position (row, col) of variables in the sudoku board.

        neighbours:
            list of sets for each variable containing the indices of the neighbours for the variable.
            var_i_idx = var_i_neighbours_idx
        
        domain: list of lists.
            Each sublist contains the allowable values for a variable. var_i_idx = dom_of_var_i_idx.

    Output
        boolean:
            True if arcs are now consistent. False if not / sudoku is not solvable.
    """

    # Queue of all the arcs to revise the domain against
    agenda = Queue()

    # 0. Get the neighbours of each variable
    neighbours = get_neighbour_nodes(variables)

    # 1. Add all arcs (relation between neighbours) between variables to the agenda.
    for var_i, var_i_neighbours in neighbours.items():

        # parse variable index from string -> integer
        for var_j in var_i_neighbours:

                # vars represented by their indicies in the 'variables' list
                arc = (var_i, var_j) 
                agenda.enqueue(arc)

    # 2. Repeat until the arc agenda is empty:
    while agenda.size() != 0:

        # 2.1. Dequeue  (Xi, Xj) from the agenda.
        (var_i, var_j) = agenda.dequeue()

        # 2.2. For every value of the doamin of var_i there must be a value of var_j that satisfies the constraint.
        #     Revise the domain of var i so this is true.
        if revise_domain(sudoku, domains, var_i, var_j):
            
            # 2.3. If this new domain is empty, there are no legal values for var i. 
            if len(domains[var_i]) == 0:

                # Sudoku is unsolvable if a variable has no domain.
                return False
            
            # 2.4. Change of domain -> we must revise i's neighbours with respect to i's' new domain.          
            for var_k in variables:

                # Let var_k = the neighbours of i except j (since var_i's domain is now consistent with j's.)
                if var_k != var_i and var_k != var_j:

                    arc = (var_k, var_i)
                    agenda.enqueue(arc)

    return True



def most_constrained_variable(domains: dict) -> int:
    """
    Returns the index of the variable with the smallest domain. (Minimum Remaining value)
    Input:
        domain: list of lists.
                Each sublist contains the allowable values for a variable. var_i_idx = dom_of_var_i_idx.
    Output:
        integer:
            Index of the variable with the smallest domain. Returns -1 if there are no values left
    """
    if len(domains) == 0:
        return None
    else:
        return min(domains, key = lambda i: len(domains[i]))



def backtrack_search(sudoku: object, revised_domains = None) -> bool:
    """
    A depth first search which backtracks at dead-ends and returns whether a solution could be found

    Input:
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

        revised_domains: dictionary of lists
            Each nested list contains the legal values that a variable can take.
    
    Output:
        boolean indicating whether the sudoku can be solved

    """

    variables = get_variables(sudoku)
    if revised_domains != None:
        domains = revised_domains
    else:
        domains = get_domains(sudoku, variables)
    
    var_s = most_constrained_variable(domains)
    if var_s == None:
        return True

    for possible_var_s_value in domains[var_s]:

        # assign the variable to the board
        insert_value(sudoku, var_s, possible_var_s_value, False)
        
        # ends recursion if solved
        if backtrack_search(sudoku, None):
            return True

        # resets assignment -> 0 means empty space
        insert_value(sudoku, var_s, 0)
    
    # when no values in var_s domain worked
    return False



def sudoku_solver(sudoku: object) -> object:
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """

    # 9 x 9 board: all array entries should be -1
    unsolvable_board = np.array([np.array([-1] * 9) ] * 9)

    # 0. Pre-emptive check that the board is valid
    if is_illegal_board(sudoku):
        return unsolvable_board
    
    # 1. Locate the variables on the sudoku board.
    variables = get_variables(sudoku)

    # 2. Find the legal values these variables can take -> unary constraint creates domain.
    domains = get_domains(sudoku, variables)

    # 3. Pre-emptive check that there is no variables with no domain -> no solution
    if any(map(lambda ith_domain: len(ith_domain) == 0, domains)): return unsolvable_board

    # 4. Make arcs between variables consistent:
    arcs_are_consistent = arc_consistency(sudoku, variables, domains)

    # 5. If arcs aren't consistent, board is unsolvable
    if not arcs_are_consistent: return unsolvable_board

    # 6a. If all domains are of length -> solution is found
    if  all(map(lambda ith_domain: len(ith_domain) == 1, domains.values())):

        # Construct the final solution:
        for var_i, var_i_domain in domains.items():
            insert_value(sudoku, var_i, var_i_domain[0])
    
    # 6b. If more than one value in a variables domain -> recursively make assignments with DFS
    else:

        solved = backtrack_search(sudoku, domains)
        if not solved:
            return unsolvable_board

    return sudoku