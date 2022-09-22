import copy
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

        # keep track of actions taken for adjustments of weights after game
        self.actions = []

    def place_ships(self, board):
        self.actions = []
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
        choice = random.choices(self.possible_shots, weights=shot_weights, k=1)[0]
        # save this choice and the inputs that resulted in it to adjust weights at game end
        self.actions.append([copy.copy(aiming_board), choice])
        return choice

    def game_finish(self, won):
        # if this player wins, increase the likelihood of each action taken in this game being taken again if the
        # same inputs are received
        if won:
            for action in self.actions:
                for i in range(len(action[0].hits)):
                    self.hits_weights[i] -= 5
                    self.hits_weights[i][action[1]] += 105
                for i in range(len(action[0].misses)):
                    self.misses_weights[i] -= 5
                    self.misses_weights[i][action[1]] += 105
        # decrease them if this player lost
        else:
            for action in self.actions:
                for i in range(len(action[0].hits)):
                    self.hits_weights[i] += 5
                    self.hits_weights[i][action[1]] -= 105
                for i in range(len(action[0].misses)):
                    self.misses_weights[i] += 5
                    self.misses_weights[i][action[1]] -= 105
