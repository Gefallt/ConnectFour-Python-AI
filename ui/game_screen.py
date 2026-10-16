import tkinter as tk
import os
import torch

from models.board import ROWS, COLS
from models.board import Board
from models.ai import EasyAI
from models.ai import MediumAI
from models.ai import HardAI
from models.ai import NeuralAI
from models.connect4net import Connect4Net
from models.trainer import Trainer

#>>>
ACTION_1 = "history ="
#<<<
class GameScreen:

    CELL_SIZE = 80

    def __init__(self, root, settings):
#>>>>        
#        self.ai_vs_ai = True
#<<<<
        self.root = root
        self.settings = settings

        self.board = Board()

        self.current_player = 1

        self.move_history = []

        self.replay_index = 0
        self.replay_running = False
#>>>        
        self.game_over = False
#<<<
        window_width = COLS * self.CELL_SIZE + 40
        window_height = ROWS * self.CELL_SIZE + 320             #<<<230

        self.root.title("Connect Four")
        self.root.geometry(
            f"{window_width}x{window_height}"
        )
#>>>
#        self.info_label = tk.Label(
#            root,
#            text=f"P1:{settings.player1_type}  vs  P2:{settings.player2_type}"
#        )
#<<<
#>>>
#        self.info_label.pack(pady=10)
#<<<>>>>
        # ----------------------------
        # Information Area
        # ----------------------------

        self.player_label = tk.Label(
            root,
            text=f"P1:{settings.player1_type}  vs  P2:{settings.player2_type}",
            font=("Arial", 10, "bold")
        )
        self.player_label.pack(pady=(10, 0))

        self.turn_label = tk.Label(
            root,
            text="Turn : Red",
            fg="blue"
        )
        self.turn_label.pack()

        self.result_label = tk.Label(
            root,
            text="Result : ",
            fg="green"
        )
        self.result_label.pack()

        self.training_label = tk.Label(
            root,
            text="Training : Ready",
            justify="left",
            anchor="w"
        )
        self.training_label.pack()
#<<<<<<<
        self.canvas = tk.Canvas(
            root,
            width=COLS * self.CELL_SIZE,
            height=ROWS * self.CELL_SIZE,
            bg="navy"
        )

        self.canvas.pack(pady=10)

        self.canvas.bind(
            "<Button-1>",
            self.on_click
        )

        # Replay Buttons

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=5)

        tk.Button(
            self.control_frame,
            text="|<",
            width=4,
            command=self.first_move
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            self.control_frame,
            text="<",
            width=4,
            command=self.prev_move
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            self.control_frame,
            text="■",
            width=4,
            command=self.stop_replay
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            self.control_frame,
            text=">",
            width=4,
            command=self.next_move
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            self.control_frame,
            text=">|",
            width=4,
            command=self.start_replay
        ).pack(side=tk.LEFT, padx=2)

        # Game Buttons

        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack(pady=10)

        tk.Button(
            self.menu_frame,
            text="New Game",
            width=12,
            command=self.new_game
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.menu_frame,
            text="Back To Menu",
            width=12,
            command=self.back_to_menu
        ).pack(side=tk.LEFT, padx=5)

        self.draw_board()
#>>>
        if not self.is_human(self.current_player):
            self.root.after(
                500,
                self.computer_move
            )
#<<<

    def draw_board(self):
        self.canvas.delete("all")

        for row in range(ROWS):
            for col in range(COLS):

                x1 = col * self.CELL_SIZE + 5
                y1 = row * self.CELL_SIZE + 5

                x2 = x1 + self.CELL_SIZE - 10
                y2 = y1 + self.CELL_SIZE - 10

                color = "white"

                cell = self.board.grid[row][col]

                if cell == 1:
                    color = "red"

                elif cell == 2:
                    color = "yellow"

                self.canvas.create_oval(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color
                )
#>>>>>>>
#        self.training_label.config(
#            text=
#            f"Training:\n"
#            f"Moves : {len(self.move_history)}\n"
#            f"Current Player : {self.current_player}"
#        )
        state_text = (
            "Game Over"
            if self.game_over
            else "Playing"
        )

        player_name = (
            "Red"
            if self.current_player == 1
            else "Yellow"
        )

        last_move = (
            self.move_history[-1]
            if self.move_history
            else "-"
        )

        self.training_label.config(
            text=
            f"Training:\n"
            f"Moves : {len(self.move_history)}\n"
            f"State : {state_text}\n"
            f"Turn : {player_name}\n"
            f"Last Move : {last_move}\n"
            f"History : {self.move_history}"
        )
#<<<<<<<
    def on_click(self, event):
#>>>        
        if self.game_over:
            return
#<<<
        if self.replay_running:
            return
#>>>
        if not self.is_human(self.current_player):
            return
#<<<
        col = event.x // self.CELL_SIZE

        if col < 0 or col >= COLS:
            return

        row = self.board.drop_piece(
            col,
            self.current_player                           #<<<"1" 
        )

        if row < 0:
            return

        self.move_history.append(col)

        print(ACTION_1, self.move_history)

        self.draw_board()

        if self.board.has_player_won(
            self.current_player,                          #<<<"1"
            col,
            row
        ):
            winner_type = self.get_player_type(
                self.current_player
            )
#>>>>>>>
#            self.info_label.config(
#                text=f"{winner_type}(Red)Wins!"
#            )
            winner_color = (
                "Red"
                if self.current_player == 1
                else "Yellow"
            )

            self.result_label.config(
                text=f"Result : {winner_type} ({winner_color}) Wins!"
            )

#            self.create_initial_model()                    ######
            trainer = Trainer()

            trainer.train_from_history(
            self.move_history
            )

#<<<<<<<            
#>>>            
            self.game_over = True
            self.draw_board()
#<<<
            return
#>>>
        self.current_player = (
            2 if self.current_player == 1
            else 1
        )
#>>>>>>>        
        self.update_turn_label()
#<<<<<<<        
        if not self.is_human(self.current_player):
            self.root.after(
                300,
                self.computer_move
            )
#<<<

    # ----------------------------
    # Replay
    # ----------------------------

    def rebuild_board(self):

        self.board = Board()

        player = 1

        for i in range(self.replay_index):

            col = self.move_history[i]

            self.board.drop_piece(
                col,
                player
            )

            player = (
                2 if player == 1
                else 1
            )

        self.draw_board()

    def first_move(self):

        self.stop_replay()

        self.replay_index = 0

        self.rebuild_board()
#>>>>>>>
#        self.info_label.config(
#            text="Start Position"
#        )
        self.result_label.config(
            text="Result : Start Position"
        )
#<<<<<<<

    def prev_move(self):

        self.stop_replay()

        if self.replay_index > 0:

            self.replay_index -= 1

            self.rebuild_board()
#>>>>>>>
#            self.info_label.config(
#                text=f"Move {self.replay_index}"
#            )
            self.result_label.config(
                text=f"Result : Move {self.replay_index}"
            )
#<<<<<<<
    def next_move(self):

        self.stop_replay()

        if self.replay_index < len(self.move_history):

            self.replay_index += 1

            self.rebuild_board()
#>>>>>>>
#            self.info_label.config(
#                text=f"Move {self.replay_index}"
#            )
            self.result_label.config(
                text=f"Result : Move {self.replay_index}"
            )
#<<<<<<<
    def stop_replay(self):

        self.replay_running = False

    def start_replay(self):

        print("Replay History:")
        print(self.move_history)

        if len(self.move_history) == 0:
            return

        self.replay_running = True

        self.replay_index = 0

        self.board = Board()

        self.draw_board()

        self.auto_play()

    def auto_play(self):

        if not self.replay_running:
            return

        if self.replay_index > len(self.move_history):

            self.replay_running = False
#>>>>>>>
#            self.info_label.config(
#                text="Replay Finished"
#            )
            self.result_label.config(
            text="Result : Replay Finished"
        )
#<<<<<<<
            return

        self.rebuild_board()

        self.replay_index += 1

        self.root.after(
            500,
            self.auto_play
        )

    # ----------------------------
    # New Game
    # ----------------------------

    def new_game(self):

        self.stop_replay()
#>>>            
        self.game_over = False
#<<<           
        self.board = Board()

        self.current_player = 1

        self.move_history = []

        self.replay_index = 0
#>>>>>>>
#        self.info_label.config(
#            text=f"P1:{self.settings.player1_type}  vs  P2:{self.settings.player2_type}"
#        )
        self.player_label.config(
            text=f"P1:{self.settings.player1_type}  vs  P2:{self.settings.player2_type}"
        )
        
        self.turn_label.config(
            text="Turn : Red"
        )

        self.result_label.config(
            text="Result : "
        )

        self.training_label.config(
            text="Training : Ready"
        )
#<<<<<<<
        self.draw_board()
#>>>
        if not self.is_human(self.current_player):
            self.root.after(
                500,
                self.computer_move
            )
#<<<
        print("New Game Started")

    # ----------------------------
    # Back To Menu
    # ----------------------------

    def back_to_menu(self):

        self.stop_replay()

        for widget in self.root.winfo_children():
            widget.destroy()

        # 循環参照回避
        from ui.start_screen import StartScreen

        StartScreen(self.root)
        
    # ----------------------------
    # AI select
    # ----------------------------

    def computer_move(self):
#>>>
        player_type = self.get_player_type(
            self.current_player
        )

        ai = self.create_ai(player_type)

        if ai is None:
            return
#<<<
        col = ai.choose_move()

        row = self.board.drop_piece(
            col,
            self.current_player
        )

        if row < 0:
            return

        self.move_history.append(col)

        print(ACTION_1, self.move_history)

        self.draw_board()

        if self.board.has_player_won(
            self.current_player,
            col,
            row
        ):
#>>>>>>>
#            winner = (
#               "Red"
#                if self.current_player == 1
#                else "Yellow"
#            )
#            self.info_label.config(
#                text=f"{winner} Wins!"
#            ) 
#            self.result_label.config(
#                text=f"Result : {winner} Wins!"
#            )
            winner_type = self.get_player_type(
                self.current_player
            )

            winner_color = (
                "Red"
                if self.current_player == 1
                else "Yellow"
            )

            self.result_label.config(
                text=f"Result : {winner_type} ({winner_color}) Wins!"
            )

#            self.create_initial_model()                    ######
            trainer = Trainer()

            trainer.train_from_history(
            self.move_history
)

#<<<<<<<
#>>>            
            self.game_over = True
            self.draw_board()
#<<<           
            return

#>>>
        self.current_player = (
            2 if self.current_player == 1
            else 1
        )
#>>>>>>>        
        self.update_turn_label()
#<<<<<<<        
        if not self.is_human(self.current_player):
            self.root.after(
                300,
                self.computer_move
            )
#<<<
    # ----------------------------
#>>># Helper
    # ----------------------------
    def get_player_type(self, player_no):

        if player_no == 1:
            return self.settings.player1_type

        return self.settings.player2_type
#<<<

#>>>
    # ----------------------------
    # AI 取得用メソッド
    # ----------------------------
    def create_ai(self, player_type):

        if player_type == "AI-Easy":
            return EasyAI(self.board)

        elif player_type == "AI-Medium":
            return MediumAI(self.board)

        elif player_type == "AI-Hard":
            return HardAI(self.board)

        elif player_type == "AI-Neural":
            return NeuralAI(self.board)

        return None
#<<<
#>>>
    # ----------------------------
    #  Human / AI 判定
    # ----------------------------
    def is_human(self, player_no):

        if player_no == 1:
            return self.settings.player1_type == "Human"

        return self.settings.player2_type == "Human"
#<<<
#>>>>>>>
    # ----------------------------
    #  手番表示更新用メソッド
    # ----------------------------
    def update_turn_label(self):

        color = (
            "Red"
            if self.current_player == 1
            else "Yellow"
        )

        self.turn_label.config(
            text=f"Turn : {color}"
        )
#<<<<<<<
    # ----------------------------
    #  初期pth作成メソッド
    # ----------------------------

    def create_initial_model(self):

        os.makedirs(
            "saved",
            exist_ok=True
        )

        if not os.path.exists(
            "saved/connect4_model.pth"
        ):

            model = Connect4Net()

            torch.save(
                model.state_dict(),
                "saved/connect4_model.pth"
            )

            print(
                "Initial Neural Model Created."
            )
