from itertools import product

import pygame
from pygame import Surface

from src.ai import AI
from src.boardstate import BoardState
import time

def draw_board(screen: Surface, pos_x: int, pos_y: int, elem_size: int, board: BoardState):
    darker = (150, 150, 150)
    lighter = (160, 160, 160)
    white = (255, 255, 255)
    black = (0, 0, 0)

    for y, x in product(range(15), range(15)):
        color = lighter if (x + y) % 2 == 0 else darker
        position = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size
        pygame.draw.rect(screen, color, position)

        figure = board.board[y, x]

        if figure == 0:
            continue

        if figure > 0:
            figure_color = white
        else:
            figure_color = black
        r = elem_size // 2 - 10

        pygame.draw.circle(screen, figure_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r)

def change_caption(board, MODE):
    if board.winner == 0:
        if board.current_player > 0:
            if MODE == "player":
                line = "White move"
            elif MODE == "ai":
                line = "Your move"
            if board.white_open_pattern:
                if MODE == "player":
                    line += " : White have almost won"
                elif MODE == "ai":
                    line += " : You have almost won"
            pygame.display.set_caption(TITLE + line)
        else:
            line = "Black move"
            if board.white_open_pattern:
                line += " : Black have almost won"
            pygame.display.set_caption(TITLE + line)
    else:
        if board.winner > 0:
            pygame.display.set_caption(TITLE + "White wins the game!!!")
        else:
            pygame.display.set_caption(TITLE + "Black wins the game!!!")

def game_loop(screen: Surface, board: BoardState, ai: AI):
    grid_size = screen.get_size()[0] // 15
    choosing_mode = True
    while choosing_mode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    MODE = MODES[1]
                    choosing_mode = False
                if event.key == pygame.K_p:
                    choosing_mode = False
                    MODE = MODES[0]
    if MODE == MODES[0]:
        pygame.display.set_caption(TITLE + "White move")
        print("2 players mode")
    if MODE == MODES[1]:
        pygame.display.set_caption(TITLE + "Player`s move")
        print("1 player mode")
    pygame.display.update()
    pause_for_player = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("game has been finished")
                return
            if board.winner == 0:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if MODE == MODES[0]:
                        x_pos, y_pos = [p // grid_size for p in event.pos]
                        position = [x_pos, y_pos]
                        board.do_move(position)
                        if board.winner != 0:
                            print("There is a winner in a game:" + str(board.winner))
                        change_caption(board)
                    if MODE == MODES[1]:
                        x_pos, y_pos = [p // grid_size for p in event.pos]
                        position = [x_pos, y_pos]
                        if not pause_for_player:
                            if board.do_move(position):
                                if board.winner == 0:
                                    pause_for_player = True
                                    board = ai.do_move(board, depth=2)
                                    if board.winner != 0:
                                        print("There is a winner in a game:" + str(board.winner))
                                    pause_for_player = False
                                change_caption(board, MODE)
            else:
                print("Moves are not allowed\nThere is a winner in a game: " + str(board.winner))

        draw_board(screen, 0, 0, grid_size, board)
        pygame.display.flip()


pygame.init()
print("game gui has been initialized")
TITLE = "Gomoku : "
SIZE = [615, 615]
MODES = ["player", "ai", "ai_vs_ai"]
MODE = ""
screen: Surface = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE + "Choose game mode (press key P or A)")
pygame.display.update()
ai = AI(search_depth=4, color=-1)

game_loop(screen, BoardState.initial_state(), ai)

pygame.quit()
