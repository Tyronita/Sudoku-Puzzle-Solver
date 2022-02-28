import time, numpy as np
from sudoku import sudoku_solver

def main():

    for difficulty in ['very_easy', 'easy', 'medium', 'hard']:

        print(f"Testing {difficulty} sudokus")
        
        # import sudokus and solutions from numpy vector files
        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")
        
        # initialise a count for correct solutions
        count = 0

        for i in range(len(sudokus)):

            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)
            
            # take start and end timesamps for before/after solving the current sudoku puzzle
            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()
            
            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)
            
            print("Is the solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])
            
            print("This sudoku took", end_time-start_time, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break

if __name__ == "__main__":
    main()