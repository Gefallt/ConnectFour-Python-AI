import torch

class TrainedAI:

    def __init__(self, board):

        self.board = board

        self.model_path = (
            "saved/connect4_model.pth"
        )

    def choose_move(self):

        data = torch.load(
            self.model_path
        )

        preferred_col = data[
            "preferred_column"
        ]

        return preferred_col

