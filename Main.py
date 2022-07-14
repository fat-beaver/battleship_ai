import AIPlayer
import Game

player1 = AIPlayer.AIPlayer(Game.BOARD_WIDTH, Game.BOARD_HEIGHT)
player2 = Game.Player(Game.BOARD_WIDTH, Game.BOARD_HEIGHT)

game = Game.BattleshipGame(player1, player2)
aiming_board = game.player1_aiming_board

for i in range(100000):
    player1.take_shot(aiming_board)

print(player1.take_shot(aiming_board))
