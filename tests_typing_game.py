import time
import pytest

from gui import Level
from typing_game import calculate_accuracy, read_sentences_from_file, TypingGame


def test_calculate_accuracy():
    accuracy = calculate_accuracy("Hello", "Hello")
    assert accuracy == 100

    accuracy = calculate_accuracy("Hello", "World")
    assert accuracy == 20

    accuracy = calculate_accuracy("Hello", "Abracadabra")
    assert accuracy == 0


def test_read_sentences_from_file():
    sentences = read_sentences_from_file('./texts/sample.txt')
    expected_sentences = ["This is the first sentence", "This is the second sentence", "This is the third sentence",
                          "This is the fourth sentence"]
    assert sentences == expected_sentences


def test_typing_game_start_timer():
    game = TypingGame()
    game.timer_thread.remaining_time = 10

    game.start_timer()
    time.sleep(2)

    assert game.timer_thread.is_running  # Timer thread should be running
    assert game.timer_thread.remaining_time < 10  # Remaining time should be lower than 10 seconds


def test_typing_game_stop_timer():
    diff = Level.EASY
    game = TypingGame(diff)
    game.timer_thread.remaining_time = 10

    game.stop_timer()
    time.sleep(2)

    assert not game.timer_thread.is_running  # Timer thread should be stopped
    assert game.timer_thread.remaining_time == 10  # Remaining time should not be changed


def test_typing_game_restart_game():
    diff = Level.EASY
    game = TypingGame(diff)
    game.sentences = ["Sentence 1", "Sentence 2", "Sentence 3"]
    game.sentence_iterator = iter(game.sentences)
    game.current_sentence = next(game.sentence_iterator)
    game.user_text = "Sentence 1"
    game.total_user_input = ["Sentence 1"]
    game.total_expected_input = ["Sentence 1"]

    game.restart_game()

    assert game.current_sentence == game.sentences[0]
    assert game.user_text == ""
    assert game.total_user_input == []
    assert game.total_expected_input == []



if __name__ == '__main__':
    pytest.main()
