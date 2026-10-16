# ConnectFour AI

Python + PyTorch による Connect Four AI

## 概要

6行7列の Connect Four をプレイする AI です。

## 実行方法

```bash
pip install torch
pip install pygame

python main.py
```

## ネットワーク構成

```text
42 (盤面)
 ↓
128
 ↓
128
 ↓
64
 ↓
7 (列選択)
```

## プロジェクト構成

```text
models/
├─ connect4net.py
├─ trainer.py
├─ trained_ai.py
├─ board.py
└─ settings.py

ui/
├─ start_screen.py
└─ game_screen.py

saved/
└─ connect4_model.pth
```

## 技術

- Python 3.11
- PyTorch
- Pygame
- Reinforcement Learning