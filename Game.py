import random

import numpy as np

BOARD_WIDTH = 10
BOARD_HEIGHT = 10

SHIP_LENGTHS = [5, 4, 3, 3, 2]

TOTAL_SHIP_HEALTH = 17  # the total of the ship lengths


class GameBoard:
    def __init__(self):
        self.hits = np.array([False] * BOARD_WIDTH * BOARD_HEIGHT)
        self.misses = np.array([False] * BOARD_WIDTH * BOARD_HEIGHT)

    def __copy__(self):
        new_game_board = GameBoard()
        new_game_board.hits = self.hits.copy()
        new_game_board.misses = self.misses.copy()
        return new_game_board


class TargetBoard(GameBoard):

    def __init__(self, ship_lengths):
        # all the ships currently on this board
        super().__init__()
        self.ships = []
        # the allowed ship lengths
        self.ships_required = ship_lengths.copy()
        self.cells_containing_ships = np.array([False] * BOARD_WIDTH * BOARD_HEIGHT)

    # vertical is a bool for orientation
    def place_ship(self, x_coord, y_coord, ship_length, vertical):
        if 0 <= x_coord < BOARD_WIDTH and 0 <= y_coord < BOARD_HEIGHT and ship_length in self.ships_required:
            # remove the ship from the list of ships to add and add it to the list of ships
            self.ships_required.remove(ship_length)
            self.ships.append([x_coord, y_coord, ship_length, vertical])
            # determine which cells this ship occupies
            if vertical:
                for i in range(ship_length):
                    self.cells_containing_ships[(i + y_coord) * BOARD_WIDTH + x_coord] = True
            else:
                for i in range(ship_length):
                    self.cells_containing_ships[BOARD_WIDTH * y_coord + x_coord + i] = True

    def ships_to_place(self):
        return len(self.ships_required)

    # cell number is from 0 to (board_width * board_height - 1)
    def check_hit(self, cell_number):
        return self.cells_containing_ships[cell_number]


class Player:
    def __init__(self, board_width, board_height, ships):
        self.board_width = board_width
        self.board_height = board_height
        self.ships = ships.copy()

    def place_ships(self, board):
        pass

    def take_shot(self, aiming_board):
        pass

    def game_finish(self, won):
        pass


class BattleshipGame:

    def __init__(self, player1, player2):
        # randomly select which player takes which slot, so a player cannot develop a strategy reliant on playing first
        if bool(random.getrandbits(1)):
            self.player1 = player1
            self.player2 = player2
        else:
            self.player1 = player2
            self.player2 = player1
        # both boards for each player, not stored as part of the player to stop cheating
        self.player1_aiming_board = GameBoard()
        self.player1_target_board = TargetBoard(SHIP_LENGTHS)

        self.player2_aiming_board = GameBoard()
        self.player2_target_board = TargetBoard(SHIP_LENGTHS)

    def start_game(self):
        # order both players to set up their ships
        self.player1.place_ships(self.player1_target_board)
        self.player2.place_ships(self.player2_target_board)

        # keep track of how much health each fleet has remaining
        player1_hits_remaining = TOTAL_SHIP_HEALTH
        player2_hits_remaining = TOTAL_SHIP_HEALTH

        player_one_turn = True

        turns_taken = 0

        while player1_hits_remaining > 0 and player2_hits_remaining > 0:
            if player_one_turn:
                turns_taken += 1
                shot_taken = self.player1.take_shot(self.player1_aiming_board)
                if self.player2_target_board.check_hit(shot_taken):
                    # on a hit, update the boards and remove one health from the opposing fleet
                    self.player1_aiming_board.hits[shot_taken] = True
                    self.player2_target_board.hits[shot_taken] = True
                    player2_hits_remaining -= 1
                else:
                    # on a miss, only update the boards
                    self.player1_aiming_board.misses[shot_taken] = True
                    self.player2_target_board.misses[shot_taken] = True
            else:
                shot_taken = self.player2.take_shot(self.player2_aiming_board)
                if self.player1_target_board.check_hit(shot_taken):
                    # on a hit, update the boards and remove one health from the opposing fleet
                    self.player2_aiming_board.hits[shot_taken] = True
                    self.player1_target_board.hits[shot_taken] = True
                    player1_hits_remaining -= 1
                else:
                    # on a miss, only update the boards
                    self.player2_aiming_board.misses[shot_taken] = True
                    self.player1_target_board.misses[shot_taken] = True

            player_one_turn = not player_one_turn

        if player1_hits_remaining == 0:
            self.player1.game_finish(False)
            self.player2.game_finish(True)
            # print("Player 2 won in " + str(turns_taken) + " rounds")
        else:
            self.player1.game_finish(True)
            self.player2.game_finish(False)
            # print("Player 1 won in " + str(turns_taken) + " rounds")
