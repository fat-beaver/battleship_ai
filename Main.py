import AIPlayer
import Game

while True:
    player1 = AIPlayer.AIPlayer(Game.BOARD_WIDTH, Game.BOARD_HEIGHT, Game.SHIP_LENGTHS)
    player2 = AIPlayer.AIPlayer(Game.BOARD_WIDTH, Game.BOARD_HEIGHT, Game.SHIP_LENGTHS)

    game = Game.BattleshipGame(player1, player2)
    game.start_game()
