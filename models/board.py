#定数　６行７列
ROWS = 6
COLS = 7


class Board:
#(method)
    def __init__(self):
        self.grid = [
            [0 for _ in range(COLS)]
            for _ in range(ROWS)
        ]
#
#(method)
    def drop_piece(self, col, player):
        for row in range(ROWS - 1, -1, -1):
            if self.grid[row][col] == 0:
                self.grid[row][col] = player
                return row
        return -1
#
#(method)
    def has_player_won(self, player, col, row):
        directions = [
            (1, 0),
            (0, 1),
            (1, 1),
            (1, -1)
        ]

        for dx, dy in directions:

            count = 1

            x = col + dx
            y = row + dy

            while (
                0 <= x < COLS
                and 0 <= y < ROWS
                and self.grid[y][x] == player
            ):
                count += 1
                x += dx
                y += dy

            x = col - dx
            y = row - dy

            while (
                0 <= x < COLS
                and 0 <= y < ROWS
                and self.grid[y][x] == player
            ):
                count += 1
                x -= dx
                y -= dy

            if count >= 4:
                return True

        return False
#    
#(method)
    def is_column_full(self, col):
        return self.grid[0][col] != 0
#
#(method)
    def is_full(self):
        for col in range(COLS):
            if not self.is_column_full(col):
                return False
        return True
#
#(method)
    def remove_piece(self, col, row):
        self.grid[row][col] = 0
#
#(method)
    def get_player_at(self, col, row):
        return self.grid[row][col]
#
#(method)
    def copy(self):
        board = Board()
        board.grid = [
            row.copy()
            for row in self.grid
        ]
        return board
#