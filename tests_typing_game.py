import time

import pytest
from typing_game import calculate_accuracy, read_sentences_from_file, TypingGame
import texts


def test_calculate_accuracy():
    accuracy = calculate_accuracy("Hello", "Hello")
    assert accuracy == 100

    accuracy = calculate_accuracy("Hello", "World")
    assert accuracy == 20

    accuracy = calculate_accuracy("Hello", "Abracadabra")
    assert accuracy == 0


def test_read_sentences_from_file():
    sentences = read_sentences_from_file('./texts/sample.txt')
    expected_sentences = ["This is the first sentence.", "This is the second sentence.", "This is the third sentence.",
                          "This is the fourth sentence."]
    assert sentences == expected_sentences


def test_typing_game_start_timer():
    game = TypingGame()
    game.timer_thread.remaining_time = 10

    game.start_timer()
    time.sleep(2)

    assert game.timer_thread.is_running  # Timer thread should be running
    assert game.timer_thread.remaining_time < 10  # Remaining time should be lower than 10 seconds


def test_typing_game_stop_timer():
    game = TypingGame()
    game.timer_thread.remaining_time = 10

    game.stop_timer()
    time.sleep(2)

    assert not game.timer_thread.is_running  # Timer thread should be stopped
    assert game.timer_thread.remaining_time == 10  # Remaining time should not be changed


if __name__ == '__main__':
    pytest.main()
