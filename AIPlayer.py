import random
import numpy as np
import Game


class AIPlayer(Game.Player):
    def __init__(self, board_width, board_height, ships):
        super().__init__(board_width, board_height, ships)

        # create base weights, eventually these will be loaded from file
        self.starting_weights = np.array([0.001] * board_width * board_height)
        self.hits_weights = np.array([[1000] * board_width * board_height] * board_width * board_height)
        self.misses_weights = np.array([[1000] * board_width * board_height] * board_width * board_height)
        # create a list of numbers to represent each cell which may be fired upon
        self.possible_shots = range(board_width * board_height)

    def place_ships(self, board):
        for i in range(len(self.ships)):
            board.place_ship(i, 0, self.ships[i], True)

    def take_shot(self, aiming_board):
        # add an initial weight to each cell
        shot_weights = self.starting_weights.copy()
        # figure out the weights for each cell
        for i in range(len(aiming_board.hits)):
            shot_weights += aiming_board.hits * self.hits_weights[i]
            shot_weights += aiming_board.misses * self.misses_weights[i]
        # remove cells which have already been fired upon
        shot_weights *= ~aiming_board.hits
        shot_weights *= ~aiming_board.misses

        # print("hits")
        # print(aiming_board.hits)
        # print("misses")
        # print(aiming_board.misses)
        # print("weights")
        # print(shot_weights)
        return random.choices(self.possible_shots, weights=shot_weights, k=1)[0]

    def game_finish(self, won):
        pass
