from typing import Optional

from .boardstate import BoardState

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
        for i in range(15):
            for j in range(15):
                position = [i, j]
                if board.validate_move_by_position(position):
                    positions.append(position)
        return positions

    def next_move_minimax(self, board, current_depth, maximize):
        if current_depth == 1 or board.winner != 0:
            return self.evaluate_position(board)
        else:
            if maximize:
                maxEvaluation = -self.Inf
                for position in self.get_all_possible_positions(board):
                    board_copy = board.copy()
                    board_copy.do_move(position)
                    evaluation = self.next_move_minimax(board_copy, current_depth - 1, False)
                    maxEvaluation = max(evaluation, maxEvaluation)
                return maxEvaluation
            else:
                minEvaluation = self.Inf
                for position in self.get_all_possible_positions(board):
                    board_copy = board.copy()
                    board_copy.do_move(position)
                    evaluation = self.next_move_minimax(board_copy, current_depth - 1, True)
                    minEvaluation = min(evaluation, minEvaluation)
                return minEvaluation

    def do_move(self, board, depth):
        """
        position = [random.randint(0, 14), random.randint(0, 14)]
        while not board.validate_move_by_position(position):
            position = [random.randint(0, 14), random.randint(0, 14)]
        board.do_move(position)
        """

        maxEval = -self.Inf
        for position in self.get_all_possible_positions(board):
            board_copy = board.copy()
            board_copy.do_move(position)
            evaluation = self.next_move_minimax(board_copy, depth - 1, False)
            if evaluation > maxEval:
                best_board = board_copy
                maxEval = evaluation
        return best_board


    def evaluate_position(self, board: BoardState):
        if self.color > 0:
            return board.longest_white_line
        else:
            return board.longest_black_line
