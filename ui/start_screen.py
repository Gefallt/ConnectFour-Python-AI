import tkinter as tk
from tkinter import ttk

from models.settings import GameSettings
from ui.game_screen import GameScreen

class StartScreen:

    PLAYER_TYPES = [
        "Human",
        "AI-Easy",
        "AI-Medium",
        "AI-Hard",
        "AI-Neural"
    ]

    def __init__(self, root):
        self.root = root

        self.root.title("Connect Four")
        self.root.geometry("400x250")

        tk.Label(
            root,
            text="Connect Four",
            font=("Segoe UI", 20)
        ).pack(pady=10)

        tk.Label(root, text="Player 1").pack()

        self.player1_type = tk.StringVar(value="Human")

        ttk.Combobox(
            root,
            textvariable=self.player1_type,
            values=self.PLAYER_TYPES,
            state="readonly"
        ).pack()

        tk.Label(root, text="Player 2").pack(pady=(10, 0))

        self.player2_type = tk.StringVar(value="AI-Hard")

        ttk.Combobox(
            root,
            textvariable=self.player2_type,
            values=self.PLAYER_TYPES,
            state="readonly"
        ).pack()

        tk.Button(
            root,
            text="Start Game",
            command=self.start_game
        ).pack(pady=30)

    def start_game(self):

        settings = GameSettings(
            player1_type=self.player1_type.get(),
            player2_type=self.player2_type.get()
        )

        for widget in self.root.winfo_children():
            widget.destroy()

        GameScreen(self.root, settings)

        print(settings)