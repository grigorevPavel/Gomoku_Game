import numpy as np
from typing import Optional, List


class BoardState:
    def __init__(self, board: np.ndarray, current_player: int = 1, borders=[15, -1, 15, -1]):
        self.board: np.ndarray = board
        self.current_player: int = current_player  # -1 - black 1 - white
        self.winner = 0
        self.longest_black_line = 0
        self.longest_white_line = 0
        self.top_most_position = borders[0]
        self.bottom_most_position = borders[1]
        self.left_most_position = borders[2]
        self.right_most_position = borders[3]
        #position [x, y]
        # print("new board has been created")

    def copy(self) -> 'BoardState':
        borders = []
        borders.append(self.top_most_position)
        borders.append(self.bottom_most_position)
        borders.append(self.left_most_position)
        borders.append(self.right_most_position)
        return BoardState(self.board.copy(), self.current_player, borders)

    def validate_move_by_position(self, position) -> bool:
        return (0 <= position[0] < 15) and (0 <= position[1] < 15) and self.board[position[1], position[0]] == 0

    def count_dimensions_of_active_zone(self):
        horizontal = abs(self.right_most_position - self.left_most_position + 1)
        vertical = abs(self.bottom_most_position - self.top_most_position + 1)
        return [horizontal, vertical]

    def create_figure(self, position, color):
        # position[x, y]
        # color = white/black
        self.board[position[1], position[0]] = color
        # while figure is being created
        self.top_most_position = min(self.top_most_position, position[1])
        self.bottom_most_position = max(self.bottom_most_position, position[1])
        self.right_most_position = max(self.right_most_position, position[0])
        self.left_most_position = min(self.left_most_position, position[0])

    def check_victory_inside_square(self, left_top_coords, color) -> bool:
        return self.check_lanes(left_top_coords, color) or self.check_diagonal_lanes(left_top_coords, color)

    def check_victory(self) -> int:
        if self.longest_black_line < 5 and self.longest_white_line < 5:
            return 0
        else:
            return 1 if self.longest_white_line == 5 else -1

    def find_longest_line_in_main_diag_of_square(self, left_top_cooords, size, color, direction=True):
        sum_diag = 0
        max_sum_diag = -1
        #left_top_coords[x, y]
        if direction:
            for i in range(size):
                if self.board[left_top_cooords[1] + i, left_top_cooords[0] + i] == color:
                    sum_diag += 1
                else:
                    max_sum_diag = max(sum_diag, max_sum_diag)
                    sum_diag = 0
        else:
            for i in range(size):
                if self.board[left_top_cooords[1] + i, left_top_cooords[0] + size - (i + 1)] == color:
                    sum_diag += 1
                else:
                    max_sum_diag = max(sum_diag, max_sum_diag)
                    sum_diag = 0
        return max_sum_diag

    def find_longest_diag(self, color):
        longest_diag = -1
        for i in range(15):
            current_diag_1 = self.find_longest_line_in_main_diag_of_square([0, 14 - i], i + 1, color, True)
            current_diag_2 = self.find_longest_line_in_main_diag_of_square([14 - i, 0], i + 1, color, True)
            current_diag_3 = self.find_longest_line_in_main_diag_of_square([0, 0], i + 1, color, False)
            current_diag_4 = self.find_longest_line_in_main_diag_of_square([14 - i, 14 - i], i + 1, color, False)
            longest_diag = max(longest_diag, current_diag_1, current_diag_2, current_diag_3, current_diag_4)
        return longest_diag

    def find_longest_lane_straight(self, color):
        sum_line, max_sum_line = 0, -1
        for line in range(self.top_most_position, self.bottom_most_position + 1):
            for col in range(self.left_most_position, self.right_most_position + 1):
                if self.board[line, col] == color:
                    sum_line += 1
                else:
                    max_sum_line = max(sum_line, max_sum_line)
                    sum_line = 0
            max_sum_line = max(sum_line, max_sum_line)
            sum_line = 0
        sum_line = 0
        for col in range(self.left_most_position, self.right_most_position + 1):
            for line in range(self.top_most_position, self.bottom_most_position + 1):
                if self.board[line, col] == color:
                    sum_line += 1
                else:
                    max_sum_line = max(sum_line, max_sum_line)
                    sum_line = 0
            max_sum_line = max(sum_line, max_sum_line)
            sum_line = 0
        return max_sum_line

    def find_longest_line(self, color):
        return max(self.find_longest_lane_straight(color), self.find_longest_diag(color))

    def update_longest_lines(self):
        self.longest_white_line = self.find_longest_line(1)
        self.longest_black_line = self.find_longest_line(-1)

    def do_move(self, position):
        if self.validate_move_by_position(position):
            self.create_figure(position, self.current_player)

            self.current_player *= -1
            self.update_longest_lines()
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
