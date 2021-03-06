import random
import numpy as np
import Game


class AIPlayer(Game.Player):
    def __init__(self, board_width, board_height):
        super().__init__(board_width, board_height)

        # create base weights, eventually these will be loaded from file
        self.starting_weights = np.array([0.001] * board_width * board_height)
        self.hits_weights = np.array([1000] * board_width * board_height)
        self.misses_weights = np.array([1000] * board_width * board_height)
        # create a list of numbers to represent each cell which may be fired upon
        self.possible_shots = range(board_width * board_height)

    def take_shot(self, aiming_board):
        # add an initial weight to each cell
        shot_weights = self.starting_weights.copy()
        # figure out the weights for each cell
        shot_weights += aiming_board.hits * self.hits_weights
        shot_weights += aiming_board.misses * self.misses_weights
        # remove cells which have already been fired upon
        shot_weights *= ~aiming_board.hits
        shot_weights *= ~aiming_board.misses

        return random.choices(self.possible_shots, weights=shot_weights, k=1)
