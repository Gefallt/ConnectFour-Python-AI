import torch
import torch.nn as nn
import torch.optim as optim

from models.board import Board
from models.connect4net import Connect4Net


class Trainer:

    MODEL_PATH = "saved/connect4_model.pth"

    def __init__(self):

        self.model = Connect4Net()

        self.model.load_state_dict(
            torch.load(
                self.MODEL_PATH,
                map_location="cpu"
            )
        )

        self.model.train()

        self.optimizer = optim.Adam(
            self.model.parameters(),
            lr=0.001,
            weight_decay=0.0001
        )

        self.criterion = nn.CrossEntropyLoss()

    def train_from_history(
        self,
        move_history
    ):
        """
        move_history
        [3,0,4,4,2,1,5]
        """

        board = Board()

        player = 1

        for move in move_history:

            #
            # 学習前の盤面
            #
            state = []

            for row in board.grid:
                for cell in row:

                    if cell == 2:
                        state.append(-1)
                    else:
                        state.append(cell)

            x = torch.tensor(
                [state],
                dtype=torch.float32
            )

            y = torch.tensor(
                [move],
                dtype=torch.long
            )

            #
            # 学習
            #
            output = self.model(x)

            loss = self.criterion(
                output,
                y
            )

            self.optimizer.zero_grad()

            loss.backward()

            self.optimizer.step()

            #
            # 次の局面へ
            #
            board.drop_piece(
                move,
                player
            )

            player = (
                2 if player == 1
                else 1
            )

        #
        # 保存
        #
        torch.save(
            self.model.state_dict(),
            self.MODEL_PATH
        )

        print(
            f"Learned {len(move_history)} moves"
        )