import typing_game
from guI import start_gui, select_difficulties_gui


def run_start():
    start_gui.StartGUI().run()


def run_select_difficulties():
    select_difficulties_gui.SelectDifficultiesGUI().run()


def run_game(difficulty_level):
    typing_game.TypingGame(difficulty_level).run()


if __name__ == '__main__':
    run_start()
