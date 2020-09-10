import numpy as np
from typing import Optional, List


class BoardState:
    def __init__(self, board: np.ndarray, current_player: int = 1):
        self.board: np.ndarray = board
        self.current_player: int = current_player  # -1 - black 1 - white
        self.winner = 0
        self.longest_black_line = 0
        self.longest_white_line = 0
        # print("new board has been created")

    def copy(self) -> 'BoardState':
        return BoardState(self.board.copy(), self.current_player)

    def validate_move_by_position(self, position) -> bool:
        return self.board[position[1], position[0]] == 0

    def create_figure(self, position, color):
        # position[x, y]
        # color = white/black
        self.board[position[1], position[0]] = color


    def check_diagonal_lanes(self, left_top_coords, color):
        first_diag = 0
        second_diag = 0
        for i in range(5):
            if self.board[left_top_coords[1] + i, left_top_coords[0] + i] == color:
                first_diag += 1 * color
        for i in range(5):
            if self.board[left_top_coords[1] + 4 - i, left_top_coords[0] + i] == color:
                second_diag += 1 * color
        if color > 0:
            self.longest_white_line = max(first_diag, second_diag, self.longest_white_line)
        if color < 0:
            self.longest_black_line = max(first_diag, second_diag, self.longest_black_line)
        return abs(first_diag) == 5 or abs(second_diag) == 5

    def check_lanes(self, left_top_coords, color):
        sum_in_line = 0
        sum_in_col = 0
        for i in range(5):
            sum_in_line = 0
            sum_in_col = 0
            for j in range(5):
                sum_in_line += self.board[left_top_coords[1] + i, left_top_coords[0] + j]
                sum_in_col += self.board[left_top_coords[1] + j, left_top_coords[0] + i]
            if color * sum_in_line == 5:
                return True
            if color * sum_in_col == 5:
                return True
        if color > 0:
            self.longest_white_line = max(sum_in_line, sum_in_col, self.longest_white_line)
        if color < 0:
            self.longest_black_line = max(sum_in_line, sum_in_col, self.longest_black_line)
        return False

    def check_victory_inside_square(self, left_top_coords, color) -> bool:
        return self.check_lanes(left_top_coords, color) or self.check_diagonal_lanes(left_top_coords, color)

    def check_victory(self) -> int:
        for i in range(11):
            for j in range(11):
                if self.check_victory_inside_square([i, j], 1):
                    return 1
                if self.check_victory_inside_square([i, j], -1):
                    return -1
        return 0

    def do_move(self, position):
        if self.validate_move_by_position(position):
            self.create_figure(position, self.current_player)

            self.current_player *= -1

            # print("set a new figure: color " + str(self.board[position[1], position[0]]) + " position " + str(position))
            self.winner = self.check_victory()
            return True
        else:
            # print("move at position: " + str(position) + " has not been validated")
            return False

    @staticmethod
    def initial_state() -> 'BoardState':
        board = np.zeros(shape=(15, 15), dtype=np.int8)
        winner = 0
        print("creating a default board")
        return BoardState(board, 1)
