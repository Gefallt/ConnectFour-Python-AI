import os
import random

import torch

from models.board import ROWS, COLS
from models.connect4net import Connect4Net


#
# BaseAI
#
class BaseAI:

    def __init__(self, board):

        self.board = board

#
# 勝ち手を探す
#
    def get_column_to_win(self, player):

        for col in range(COLS):

            if self.board.is_column_full(col):
                continue

            tmp = self.board.copy()

            row = tmp.drop_piece(
                col,
                player
            )

            if tmp.has_player_won(
                player,
                col,
                row
            ):
                return col

        return -1

#
# 空き列一覧
#
    def get_available_columns(self):

        return [
            col
            for col in range(COLS)
            if not self.board.is_column_full(col)
        ]


#
# EasyAI
#
class EasyAI(BaseAI):

    def choose_move(self):

        col = self.get_column_to_win(2)

        if col >= 0:
            return col

        col = self.get_column_to_win(1)

        if col >= 0:
            return col

        return random.choice(
            self.get_available_columns()
        )


#
# MediumAI
#
class MediumAI(BaseAI):

    def choose_move(self):

        col = self.get_column_to_win(2)

        if col >= 0:
            return col

        col = self.get_column_to_win(1)

        if col >= 0:
            return col

        return self.get_center_priority_column()

    def get_center_priority_column(self):

        center = COLS // 2

        if not self.board.is_column_full(center):
            return center

        for offset in range(1, COLS):

            left = center - offset
            right = center + offset

            if (
                left >= 0 and
                not self.board.is_column_full(left)
            ):
                return left

            if (
                right < COLS and
                not self.board.is_column_full(right)
            ):
                return right

        return random.choice(
            self.get_available_columns()
        )


#
# HardAI
#
class HardAI(BaseAI):

    def __init__(self, board):

        super().__init__(board)

        self.ai_player = 2
        self.human_player = 1

    def choose_move(self):

        best_score = -999999
        best_col = 0

        for col in range(COLS):

            if self.board.is_column_full(col):
                continue

            row = self.board.drop_piece(
                col,
                self.ai_player
            )

            score = self.minimax(
                depth=4,
                maximizing=False,
                last_col=col,
                last_row=row
            )

            self.board.remove_piece(
                col,
                row
            )

            if score > best_score:

                best_score = score
                best_col = col

        return best_col

    def minimax(
        self,
        depth,
        maximizing,
        last_col,
        last_row
    ):

        if self.board.has_player_won(
            self.ai_player,
            last_col,
            last_row
        ):
            return 1000 + depth

        if self.board.has_player_won(
            self.human_player,
            last_col,
            last_row
        ):
            return -1000 - depth

        if depth == 0 or self.board.is_full():
            return self.evaluate_board()

#
# MAX
#
        if maximizing:

            best = -999999

            for col in range(COLS):

                if self.board.is_column_full(col):
                    continue

                row = self.board.drop_piece(
                    col,
                    self.ai_player
                )

                score = self.minimax(
                    depth - 1,
                    False,
                    col,
                    row
                )

                self.board.remove_piece(
                    col,
                    row
                )

                best = max(
                    best,
                    score
                )

            return best

#
# MIN
#
        best = 999999

        for col in range(COLS):

            if self.board.is_column_full(col):
                continue

            row = self.board.drop_piece(
                col,
                self.human_player
            )

            score = self.minimax(
                depth - 1,
                True,
                col,
                row
            )

            self.board.remove_piece(
                col,
                row
            )

            best = min(
                best,
                score
            )

        return best

    def evaluate_board(self):

        score = 0

        center = COLS // 2

        for row in range(ROWS):

            if (
                self.board.grid[row][center]
                == self.ai_player
            ):
                score += 6

#
# 横
#
        for row in range(ROWS):
            for col in range(COLS - 3):

                window = [
                    self.board.grid[row][col+i]
                    for i in range(4)
                ]

                score += self.score_window(
                    window
                )

#
# 縦
#
        for col in range(COLS):
            for row in range(ROWS - 3):

                window = [
                    self.board.grid[row+i][col]
                    for i in range(4)
                ]

                score += self.score_window(
                    window
                )

#
# 右下
#
        for row in range(ROWS - 3):
            for col in range(COLS - 3):

                window = [
                    self.board.grid[row+i][col+i]
                    for i in range(4)
                ]

                score += self.score_window(
                    window
                )

#
# 右上
#
        for row in range(3, ROWS):
            for col in range(COLS - 3):

                window = [
                    self.board.grid[row-i][col+i]
                    for i in range(4)
                ]

                score += self.score_window(
                    window
                )

        return score

    def score_window(self, window):

        ai_count = window.count(
            self.ai_player
        )

        opponent_count = window.count(
            self.human_player
        )

        empty_count = window.count(0)

        if ai_count == 4:
            return 100000

        if opponent_count == 4:
            return -100000

        if (
            ai_count == 3 and
            empty_count == 1
        ):
            return 100

        if (
            ai_count == 2 and
            empty_count == 2
        ):
            return 10

        if (
            opponent_count == 3 and
            empty_count == 1
        ):
            return -120

        if (
            opponent_count == 2 and
            empty_count == 2
        ):
            return -10

        return 0


#
# NeuralAI
#
class NeuralAI(BaseAI):

    def __init__(self, board):

        super().__init__(board)

        self.model = Connect4Net()

        if os.path.exists(
            "saved/connect4_model.pth"
        ):

            self.model.load_state_dict(
                torch.load(
                    "saved/connect4_model.pth",
                    map_location="cpu"
                )
            )

        self.model.eval()

    def board_to_tensor(self):

        state = []

        for row in range(ROWS):
            for col in range(COLS):

                value = self.board.grid[row][col]

                if value == 2:
                    value = -1

                state.append(value)

        return torch.tensor(
            state,
            dtype=torch.float32
        ).unsqueeze(0)

    def neural_move(self):

        state = self.board_to_tensor()

        with torch.no_grad():

            scores = self.model(
                state
            )[0]

        best_col = -1
        best_score = -999999

        for col in range(COLS):

            if self.board.is_column_full(col):
                continue

            score = scores[col].item()

            if score > best_score:

                best_score = score
                best_col = col

        return best_col

    def choose_move(self):

#
# ConnectFourルールは共通利用
#

        col = self.get_column_to_win(2)

        if col >= 0:
            return col

        col = self.get_column_to_win(1)

        if col >= 0:
            return col

#
# NN判断
#

        return self.neural_move()

