import copy
import sys  # for quit the app
import time
from turtle import pos
import pygame
import numpy as np

# -----------design----------------
WIDTH = 600
HEIGHT = 600

ROWS = 3
COLS = 3
SQSIZE = WIDTH // COLS

LINE_WIDTH = 15
CIRC_WIDTH = 15
CROSS_WIDTH = 20

RADIUS = SQSIZE // 4
OFFSET = 50

BG_COLOR = (205, 192, 176)
LINE_COLOR = (139, 131, 120)
CIRC_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
# ----------------------------------

# PYGAME SETUP alwase the same code
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)
# ------------varibels----------------------
alpha = -100
beta = 100
depth = 0
size = 0


class Board:

    def __init__(self):
        # two dimintion array full with zeros using numpy
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares  # att will = empty array
        self.marked_sqrs = 0  # att for

    # return 0 if no win yet not draw , return 1 if player 1 win , 2 for player 2 win
    def final_state(self, show=False):

        # checking vertcal wins
        for col in range(COLS):
            # if player 1 win it will be 1=1=1!=0
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:  # draw winning line
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE//2, HEIGHT-20)
                    pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
                return self.squares[0][col]

        # checking horizontal win
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20,  row * SQSIZE+SQSIZE//2)
                    fPos = (WIDTH - 20, row*SQSIZE+SQSIZE//2)
                    pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
                return self.squares[row][0]

        # check diagonals win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH-20, HEIGHT-20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)

            return self.squares[1][1]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT-20)
                fPos = (WIDTH-20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # else return 0 which is no one yet win
        return 0

    # method that chanche board number from zero to player number 1 or 2
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1  # increes mared sqrs att to help us to know when our board is full

    # this method is for checking if the poss in the board is empty to mark it
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    # method to solve a broblem when want to get empty sqrs att but it is alrady marked so here we will delet every thing
    def get_empty_sqrs(self):
        empty_sqrs = []  # new att wich is empty array
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    def isfull(self):  # method will check if our att = 9 that means board is full
        return self.marked_sqrs == 9

    def isempty(self):  # the same thing as method is full
        return self.marked_sqrs == 0


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def minmax(self, board, maximizing, alpha, beta):
        global size
        # firs thing we want to check is terminal case
        case = board.final_state()

        # player one win
        if case == 1:
            return 1, None  # eval, move
        # player two win
        if case == 2:
            return -1, None

        # if draw
        elif board.isfull():
            return 0, None

        # if maximising player
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                size = size+1
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                # this is the recurgen
                eval = self.minmax(temp_board, False, alpha, beta)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                if max_eval > alpha:
                    alpha = max_eval
                if alpha >= beta:
                    return max_eval, best_move

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100  # any number creater than 1 ,0
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                size = size+1
                # we will copy the board to test it without efecting the original one
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                # this the recergen to return the eval and the best move
                eval = self.minmax(temp_board, True, alpha, beta)[0]
                if eval < min_eval:  # checking if the new eval is less than our mineval which is 100
                    min_eval = eval
                    best_move = (row, col)
                if min_eval < beta:
                    beta = min_eval
                if beta <= alpha:
                    return min_eval, best_move
            return min_eval, best_move   # return our min eval with respicting to best move

    def eval(self, main_board):  # it is the main function of AI class
        start = time.time()
        eval, move = self.minmax(main_board, False, alpha, beta)
        print(
            f'AI has chosen to mark the square in pos {move} with an eval of: {eval} ')
        end =  time.time()
        print ('whith time :' )
        print(end - start)
        print('\n----------------------------')

        return move  # it is a row and col


class Game:

    def __init__(self):  # this method will be called each time we creat an new game object
        self.board = Board()
        self.ai = AI()
        self.player = 2  # represent which player will start to play
        self.gamemode = 'ai'
        self.running = True  # this is for the game not over yet
        self.show_lines()  # call it to show new lines game

    # this method will call mark sqr to mark or check if it is avilable then it will call draw figer which will check
    def make_move(self, row, col):
        # wich player is playing now to draw x or o then call next turn to switch from 1 to 2 or 2 to 1
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):  # this method is for represent the x-o lines
        # vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0),
                         (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0),
                         (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE),
                         (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE),
                         (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):  # draw figure in the board
        if self.player == 1:  # player x
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE +
                          OFFSET)  # drawing two cross lines
            end_desc = (col * SQSIZE + SQSIZE - OFFSET,
                        row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc,
                             end_desc, CROSS_WIDTH)

            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc,
                             end_asc, CROSS_WIDTH)

        elif self.player == 2:  # player o
            center = (col * SQSIZE + SQSIZE // 2, row *
                      SQSIZE + SQSIZE // 2)  # drawing circule
            # using pygame library (draw)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def next_turn(self):  # this method is for changing players turn when self = 1 then 1%2=1+1=2 player turn and when self = 2 then 2%2=0+1=1player turn
        self.player = self.player % 2 + 1

    def isover(self):
        global depth
        depth = depth + 1
        if self.board.final_state(show=True) != 0 or self.board.isfull():
            print(
                f'The maximum depth is:{depth} \nThe number of nodes is : {size} ')
        return self.board.final_state(show=True) != 0 or self.board.isfull()


def main():

    game = Game()  # this object is from class game (our gamming object)
    board = game.board  # this is our logic board from board class
    ai = game.ai

    # -------while in the main alwase the same (main loop)---------------------------
    while True:  # this loop is counting all the event in the game like ouit app or click the screen

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # checking if some one is clicking the screen
                # this is for converting from pixel to col,row example from(388,579)to (0,0)
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                # mark this possition on the board just if it is empty
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            pygame.display.update()

            row, col = ai.eval(board)

            game.make_move(row, col)

            if game.isover():
                game.running = False

        pygame.display.update()

        print


main()
