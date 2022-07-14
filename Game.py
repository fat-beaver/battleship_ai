import numpy as np

BOARD_WIDTH = 10
BOARD_HEIGHT = 10


class GameBoard:
    hits = np.array([False] * BOARD_WIDTH * BOARD_HEIGHT)
    misses = np.array([False] * BOARD_WIDTH * BOARD_HEIGHT)


class TargetBoard(GameBoard):
    ships = np.array([False] * BOARD_WIDTH * BOARD_HEIGHT)


class Player:
    def __init__(self, board_width, board_height):
        self.board_width = board_width
        self.board_height = board_height

    def place_ships(self, ships) -> TargetBoard:
        board = TargetBoard()
        board.ships[self.board_width - ships[0]] = True
        return board

    def take_shot(self, aiming_board):
        for i in range(aiming_board.hits):
            if aiming_board[i]:
                return (i+1) * self.board_width

    def game_finish(self, won):
        if won:
            (print(self.board_width))


class BattleshipGame:
    player1_aiming_board = GameBoard()
    player1_target_board = TargetBoard()

    player2_aiming_board = GameBoard()
    player2_target_board = TargetBoard()

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
