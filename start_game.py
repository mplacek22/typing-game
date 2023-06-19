from typing_game import TypingGame


def start_game(difficulty_level):
    game = TypingGame(difficulty_level)
    game.run()