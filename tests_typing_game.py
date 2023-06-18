import time
import pytest

from gui import Level
from typing_game import calculate_accuracy, read_sentences_from_file, TypingGame


@pytest.mark.parametrize("expected_accuracy, string1, string2", [
    (100, "Hello!", "Hello!"),
    (20, "Hello", "World"),
    (0, "aaaa", "bbbb"),
    (86.21, "Hi, this is the typing game!!", "Ho,mthis is tge typing game!1"),
])
def test_calculate_accuracy(expected_accuracy, string1, string2):
    accuracy = calculate_accuracy(string1, string2)
    assert accuracy == expected_accuracy


def test_calculate_accuracy_zero_length():
    string1 = "ha ha"
    string2 = ""
    with pytest.raises(ZeroDivisionError):
        calculate_accuracy(string1, string2)


def test_calculate_accuracy_different_length():
    string1 = "Hello World"
    string2 = "Hello Worl"
    with pytest.raises(ValueError):
        calculate_accuracy(string1, string2)


def test_read_sentences_from_file():
    sentences = read_sentences_from_file('./texts/sample.txt')
    expected_sentences = ["This is the first sentence.", "This is the second sentence.", "This is the third sentence.",
                          "This is the fourth sentence."]
    assert sentences == expected_sentences


def test_typing_game_start_timer():
    game = TypingGame(Level.EASY)
    game.timer_thread.remaining_time = 10

    game.start_timer()
    time.sleep(2)

    assert game.timer_thread.is_running  # Timer thread should be running
    assert game.timer_thread.remaining_time < 10  # Remaining time should be lower than 10 seconds


def test_typing_game_stop_timer():
    game = TypingGame(Level.EASY)
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
