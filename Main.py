import AIPlayer
import Game

games_played = 0
# create the players
player1 = AIPlayer.AIPlayer(Game.BOARD_WIDTH, Game.BOARD_HEIGHT, Game.SHIP_LENGTHS)
player2 = AIPlayer.AIPlayer(Game.BOARD_WIDTH, Game.BOARD_HEIGHT, Game.SHIP_LENGTHS)

while True:
    games_played += 1

    game = Game.BattleshipGame(player1, player2)
    game.start_game()
    if games_played % 10 == 0:
        print(str(games_played) + " games played")
