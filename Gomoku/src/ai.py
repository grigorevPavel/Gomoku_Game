from typing import Optional

from src.boardstate import BoardState

import random


class AI:
    def __init__(self, search_depth: int, color: int):
        self.depth: int = search_depth
        self.color = color
        self.Inf = 999999
        print("ai has been initialized")

    def get_all_possible_positions(self, board: BoardState) -> Optional[BoardState]:
        # print("ai considers these moves to be possible at this position")
        positions = []
        for col in range(board.left_most_position - 1, board.right_most_position + 2):
            for line in range(board.top_most_position - 1, board.bottom_most_position + 2):
                position = [col, line]
                if board.validate_move_by_position(position):
                    positions.append(position)
        return positions

    def next_move_minimax(self, board, current_depth, maximize):
        if current_depth == 0 or board.winner != 0:
            return self.evaluate_position(board)

        evaluation_comparison, best_evaluation = (max, -self.Inf) if maximize else (min, self.Inf)
        for position in self.get_all_possible_positions(board):
            board_copy = board.copy()
            board_copy.do_move(position)
            evaluation = self.next_move_minimax(board_copy, current_depth - 1, not maximize)
            best_evaluation = evaluation_comparison(evaluation, best_evaluation)
        return best_evaluation

    def do_move(self, board, depth):
        """
        position = [random.randint(0, 14), random.randint(0, 14)]
        while not board.validate_move_by_position(position):
            position = [random.randint(0, 14), random.randint(0, 14)]
        board.do_move(position)
        """

        maxEval = -self.Inf - 1 # for black figures ai should maximize the evaluation
        for position in self.get_all_possible_positions(board):
            board_copy = board.copy()
            board_copy.do_move(position)
            evaluation = self.next_move_minimax(board_copy, depth - 1, False)
            if evaluation > maxEval:
                best_board = board_copy
                maxEval = evaluation
            if evaluation == self.Inf:#victory
                return best_board
        return best_board

    def look_for_open_pattern_in_square(self, board: BoardState, top_left_position, color):
        pattern = [0, color, color, color, color, 0]
        found_pattern = True
        count_in_line = 0
        count_in_col = 0
        for i in range(6):
            count_in_line = 0
            count_in_col = 0
            for j in range(6):
                if board.board[top_left_position[1] + i, top_left_position[0] + j] == pattern[j]:
                    count_in_line += 1
                if board.board[top_left_position[1] + j, top_left_position[0] + i] == pattern[j]:
                    count_in_col += 1
            if count_in_line == 6 or count_in_col == 6:
                return True
        count_in_diag_1 = 0
        count_in_diag_2 = 0
        for i in range(6):
            if board.board[top_left_position[1] + i, top_left_position[0] + i] == pattern[i]:
                count_in_diag_1 += 1
            if board.board[top_left_position[1] + i, top_left_position[0] + 5 - i] == pattern[i]:
                count_in_diag_2 += 1
        if count_in_diag_1 == 6 or count_in_diag_2 == 6:
            return True
        return False

    def look_for_open_pattern(self, board: BoardState, color):
        for line in range(10):
            for col in range(10):
                position = [col, line]
                if self.look_for_open_pattern_in_square(board, position, color):
                    return True
        return False

    def evaluate_position(self, board: BoardState):
        if board.winner == 0:
            if board.longest_white_line >= 4 or board.longest_white_line >= 4:
                if board.white_open_pattern:
                    return -self.Inf
                elif board.black_open_pattern:
                    return self.Inf
                else:
                    return board.longest_black_line - board.longest_white_line
            else:
                return board.longest_black_line - board.longest_white_line
        else:
            return -1 * board.winner * self.Inf
