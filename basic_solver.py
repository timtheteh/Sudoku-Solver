def find_next_empty(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0: # if the spot is empty, return that spot
                return row, col
    return None, None # else return None, None

def is_valid(board, num, row, col):
    # determines if num can be inserted at (row, col)
    # return True is valid, False otherwise
    
    # Check if num in row
    currentRow = board[row] # this is a list
    if num in currentRow:
        return False
    # Check if num in col
    currentCol = [board[i][col] for i in range(9)]
    if num in currentCol:
        return False
    # Check if num in small 3x3 square
    startRow = row // 3 # eg. if row is 5, x = 5//3 = 1 (second row)
    startCol = col // 3
    for i in range (startRow*3, startRow*3+3):
        for j in range (startCol*3, startCol*3+3):
            if board[i][j] == num:
                return False
    # if the num at (row, col) does not return False for any of the above checks
    # then it is a valid input
    return True

def solve(board):
    # board: 2-dimensional array (List of lists) to represent a Sudoku board
    # returns if board is solvable
    # Updates board to be solution if solution is available
    
    # find an empty spot on the board to make a guess 
    row, col = find_next_empty(board)
    
    # Terminating case: when board is full
    # if row or col is None, None --> this means the board is completely filled,
    # hence there the sudoku board is solved
    if row is None:
        return True

    # if board is not solved yet, ie. the board is not filled yet, 
    # we can continue with trying to guess values for the empty spots
    for num in range(1, 10):
        # if num can fit in the empty spot (row, col), set the value of that spot 
        # as that num, and continue solving for the rest of the empty spots 
        # by recursively calling solve()
        if is_valid(board, num, row, col):
            board[row][col] = num
            if solve(board): # this continuously updates the board with the new values
                return True # this True refers to if the terminating case is reached
            # else if the guess at (row, col) is not valid,
            # OR our guess does not solve the board
            # we will need to backtrack
            board[row][col] = 0 # resets the spot to be 0
    # if none of the numbers work, the problem is unsolvable.
    return False

def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        for j in range(len(board[i])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


# board = [
#     [7, 8, 0, 4, 0, 0, 1, 2, 0],
#     [6, 0, 0, 0, 7, 5, 0, 0, 9],
#     [0, 0, 0, 6, 0, 1, 0, 7, 8],
#     [0, 0, 7, 0, 4, 0, 2, 6, 0],
#     [0, 0, 1, 0, 5, 0, 9, 3, 0],
#     [9, 0, 4, 0, 6, 0, 0, 0, 5],
#     [0, 7, 0, 3, 0, 0, 0, 1, 2],
#     [1, 2, 0, 0, 0, 7, 4, 0, 0],
#     [0, 4, 9, 2, 0, 6, 0, 0, 7]
# ]
    

# print_board(board)
# print("-------------------------")
# solve(board)
# print_board(board)


