# ConnectFour AI

Python + PyTorch による Connect Four AI

## 実行方法

pip install torch
pip install pygame

python main.py

## 構成

models/
  connect4net.py    ニューラルネットワーク
  trainer.py        学習
  trained_ai.py     AIプレイヤー

ui/
  start_screen.py
  game_screen.py

saved/
  connect4_model.pth
``