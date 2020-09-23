import numpy as np
from typing import Optional, List


class BoardState:
    def __init__(self, board: np.ndarray, current_player: int = 1, borders=[15, -1, 15, -1],
                 longest_white=0, longest_black=0, open_white=False, open_black=False, patterns = []):
        self.board: np.ndarray = board
        self.current_player: int = current_player  # -1 - black 1 - white
        self.winner = 0
        self.longest_black_line = longest_black
        self.longest_white_line = longest_white
        self.top_most_position = borders[0]
        self.bottom_most_position = borders[1]
        self.left_most_position = borders[2]
        self.right_most_position = borders[3]
        self.black_open_pattern = open_black
        self.white_open_pattern = open_white
        self.patterns = patterns
        #position [x, y]
        # print("new board has been created")

    def copy(self) -> 'BoardState':
        borders = []
        borders.append(self.top_most_position)
        borders.append(self.bottom_most_position)
        borders.append(self.left_most_position)
        borders.append(self.right_most_position)
        return BoardState(self.board.copy(), self.current_player, borders, longest_white=self.longest_white_line,
                          longest_black=self.longest_black_line,
                          open_white=self.white_open_pattern,
                          open_black=self.black_open_pattern,
                          patterns=self.patterns)

    def validate_move_by_position(self, position) -> bool:
        return (0 <= position[0] < 15) and (0 <= position[1] < 15) and self.board[position[1], position[0]] == 0

    def validate_checkable_position(self, position, color):
        return (0 <= position[0] < 15) and (0 <= position[1] < 15) and self.board[position[1], position[0]] == color

    def count_dimensions_of_active_zone(self):
        horizontal = abs(self.right_most_position - self.left_most_position + 1)
        vertical = abs(self.bottom_most_position - self.top_most_position + 1)
        return [horizontal, vertical]

    def validate_patterns(self):
        valid_patterns = []
        self.black_open_pattern = False
        self.white_open_pattern = False
        for pattern in self.patterns:
            if self.validate_move_by_position(pattern[0][0]) and self.validate_move_by_position(pattern[0][1]):
                valid_patterns.append(pattern)
                if pattern[1] == 1:
                    self.white_open_pattern = True
                elif pattern[1] == -1:
                    self.black_open_pattern = True
        self.patterns = valid_patterns


    def check_adj_bars(self, position, color):
        #position[x, y]
        directions = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]     #[tox, to_y]
        directions_used = []
        checkable_directions = []
        for dir in directions:
            position_to = [position[0] + dir[0], position[1] + dir[1]]
            if self.validate_checkable_position(position_to, color):
                checkable_directions.append(dir)#[distance, not_used = True]
        if len(checkable_directions) == 0:
            return max(1, self.longest_white_line if color == 1 else self.longest_black_line)
        else:
            # todo
            bar_length = 1
            max_bar_length = 0
            for dir in checkable_directions:
                if dir not in directions_used:
                    opposite_dir = [dir[0] * -1, dir[1] * -1]
                    directions_used.append(dir)
                    bar_length = 1
                    dist_straight = 0
                    dist_opposite = 0
                    for i in range(4):
                        # todo
                        current_position = [position[0] + dir[0] * (i + 1), position[1] + dir[1] * (i + 1)]
                        if self.validate_checkable_position(current_position, color):
                            bar_length += 1
                            dist_straight += 1
                        else:
                            break
                    if opposite_dir in checkable_directions and opposite_dir not in directions_used:
                        directions_used.append(opposite_dir)
                        for i in range(4):
                            # todo
                            current_position = [position[0] + opposite_dir[0] * (i + 1), position[1] + opposite_dir[1] * (i + 1)]
                            if self.validate_checkable_position(current_position, color):
                                bar_length += 1
                                dist_opposite += i
                            else:
                                break
                    if bar_length == 4:
                        # look for kill pattern and a valid pattern to patterns list
                        position_start = [position[0] + dir[0] * (dist_straight + 1), position[1] + dir[1] * (dist_straight + 1)]
                        position_end = [position[0] + opposite_dir[0] * (dist_opposite + 1), position[1] + opposite_dir[1] * (dist_opposite + 1)]
                        if self.validate_move_by_position(position_start) and self.validate_move_by_position(position_end):
                            self.patterns.append([[position_start, position_end], color])
                            if color == 1:
                                self.white_open_pattern = True
                            if color == -1:
                                self.black_open_pattern = True
                max_bar_length = max(max_bar_length, bar_length)
            return max_bar_length

    def update_longest_lines(self, position, color):
        if color == -1:
            self.longest_black_line = max(self.longest_black_line, self.check_adj_bars(position, color))
        else:
            self.longest_white_line = max(self.longest_white_line, self.check_adj_bars(position, color))

    def create_figure(self, position, color):
        # position[x, y]
        # color = white/black
        self.board[position[1], position[0]] = color
        # while figure is being created
        self.top_most_position = min(self.top_most_position, position[1])
        self.bottom_most_position = max(self.bottom_most_position, position[1])
        self.right_most_position = max(self.right_most_position, position[0])
        self.left_most_position = min(self.left_most_position, position[0])

        self.validate_patterns()

        self.update_longest_lines(position, color)

    def check_victory(self) -> int:
        if self.longest_black_line < 5 and self.longest_white_line < 5:
            return 0
        else:
            return 1 if self.longest_white_line >= 5 else -1

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
