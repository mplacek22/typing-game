import start_gui
import select_difficulties_gui
import typing_game


def run_start():
    start_gui.StartGUI().run()


def run_select_difficulties():
    diff = select_difficulties_gui.SelectDifficultiesGUI()
    diff.draw()
    diff.run()


def run_game(difficulty_level):
    typing_game.TypingGame(difficulty_level).run()


if __name__ == '__main__':
    run_start()
