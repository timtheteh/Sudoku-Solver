import copy
import random
from basic_solver import is_valid, find_next_empty

class Board:
    def __init__(self, rows, cols):
        self.rows = 9
        self.cols = 9
        self.grid = [[0 for i in range(self.rows)] for j in range(self.cols)] # initialise empty grid
        self.soln_counter = 0
        self.difficulty = list(input('Difficulty (choose Easy, Medium or Hard): '))

    def get_grid(self):
        return self.grid

    def generate_filled_board(self):
        number_list = [1,2,3,4,5,6,7,8,9]
        random.shuffle(number_list)
        row, col = find_next_empty(self.grid)
        if row is None:
            return True
        for num in number_list:
            if is_valid(self.grid, num, row, col):
                self.grid[row][col] = num
                if self.generate_filled_board():
                    return True
                self.grid[row][col] = 0 #backtracking
        return False

    def remove_numbers(self):
        non_empty_squares = self.get_non_empty_squares()
        non_empty_squares_count = len(non_empty_squares)
        rounds = 3
        num_non_empty_squares = 0
        if self.difficulty == "Hard":
            num_non_empty_squares = 17
        elif self.difficulty == "Medium":
            num_non_empty_squares = 25
        else:
            num_non_empty_squares = 40
        while rounds > 0 and non_empty_squares_count >= num_non_empty_squares:
            row,col = non_empty_squares.pop(random.randrange(len(non_empty_squares)))
            non_empty_squares_count -= 1
            #might need to put the square value back if there is more than one solution
            removed_square = self.grid[row][col]
            self.grid[row][col]=0
            #make a copy of the grid to solve
            grid_copy = copy.deepcopy(self.grid)
            #initialize solutions counter to zero
            self.soln_counter = 0    
            self.solve(grid_copy)   
            #if there is more than one solution, put the last removed cell back into the grid
            if self.soln_counter!=1:
                self.grid[row][col]=removed_square
                non_empty_squares_count += 1
                rounds -=1
        return
    
    def generate_playable_board(self):
        self.generate_filled_board()
        self.remove_numbers()

    def get_non_empty_squares(self):
        list_of_non_empty_squares = []
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] != 0:
                    list_of_non_empty_squares.append((row,col))
        return list_of_non_empty_squares

    def solve(self,grid):
        row, col = find_next_empty(grid)
        if row is None:
            return True
        while True:
            for num in range(1, 10):
                if is_valid(grid, num, row, col):
                    grid[row][col] = num
                    if self.solve(grid): 
                        self.soln_counter += 1
                    grid[row][col] = 0 
            return False

    def print_board(self):
        for i in range(len(self.grid)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")
            for j in range(len(self.grid[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                if j == 8:
                    print(self.grid[i][j])
                else:
                    print(str(self.grid[i][j]) + " ", end="")