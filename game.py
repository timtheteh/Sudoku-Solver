import pygame
from solver import solve, valid
import time
from board import Board
pygame.font.init()
import pyautogui as pg

grid1 = Board(9,9)
grid1.generate_filled_board()
answer = []

for i in range(len(grid1.get_grid())):
    for j in range(len(grid1.get_grid()[0])):
        answer.append(grid1.get_grid()[i][j])

grid1.print_board()
grid1.generate_playable_board()
grid2 = grid1.get_grid()

print(answer)


class Grid:
    board = grid2

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col): 
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True  

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw(win)

def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

def main():
    win = pygame.display.set_mode((600,650))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0
    pos = list(pygame.mouse.get_pos())

    def go_right():
        clicked = board.click(tuple(pos))
        if clicked and pos[0]<450:
            board.select(clicked[0], clicked[1]+1)
            pos[0] += 60
            key = None
    
    def go_left():
        clicked = board.click(tuple(pos))
        if clicked and pos[0]>10:
            board.select(clicked[0], clicked[1]-1)
            pos[0] -= 60
            key = None

    def go_up():
        clicked = board.click(tuple(pos))
        if clicked and pos[1]>10:
            board.select(clicked[0]-1, clicked[1])
            pos[1] -= 60
            key = None
    
    def go_down():
        clicked = board.click(tuple(pos))
        if clicked and pos[1]<450:
            board.select(clicked[0]+1, clicked[1])
            pos[1] += 60
            key = None

    def go_three_right():
        pos = [0,0]
        for _ in range(3):
            clicked = board.click(tuple(pos))
            if clicked and pos[0]<450:
                board.select(clicked[0], clicked[1])
                i, j = board.selected
                print(i,j)
                board.cubes[i][j].set(answer[i*9+j])
                board.select(clicked[0], clicked[1]+1)
                pos[0] += 60
            redraw_window(win, board, play_time, strikes)
            pygame.display.update()
            pygame.time.delay(250)                

    def auto_fill():
        pos = [0,0]
        for x in range(81):
            if (x+1) % 9 != 0:
                clicked = board.click(tuple(pos))
                if clicked and pos[0]<450:
                    board.select(clicked[0], clicked[1])
                    i, j = board.selected
                    board.cubes[i][j].set(answer[i*9+j])
                    board.select(clicked[0], clicked[1]+1)
                    pos[0] += 60
                redraw_window(win, board, play_time, strikes)
                pygame.display.update()
                pygame.time.delay(1000)   
            else:
                clicked = board.click(tuple(pos))
                board.select(clicked[0], clicked[1])
                i, j = board.selected
                board.cubes[i][j].set(answer[i*9+j])
                if clicked and pos[1]<450:
                    board.select(clicked[0]+1, clicked[1])
                    pos[1] += 60
                redraw_window(win, board, play_time, strikes)
                pygame.display.update()
                pygame.time.delay(1000)
                for _ in range(9):
                    clicked = board.click(tuple(pos))
                    if clicked and pos[0]>10:
                        board.select(clicked[0], clicked[1]-1)
                        pos[0] -= 60
                redraw_window(win, board, play_time, strikes)
                pygame.display.update()
                pygame.time.delay(1000) 

    while run:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RIGHT:
                    go_right()
                if event.key == pygame.K_LEFT:
                    go_left()
                if event.key == pygame.K_UP:
                    go_up()
                if event.key == pygame.K_DOWN:
                    go_down()
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False
                if event.key == pygame.K_SPACE:
                    # go_three_right()
                    auto_fill()

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                clicked = board.click(position)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
