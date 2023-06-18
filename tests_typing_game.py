import time
import pytest
import logging
from main_gui import Level
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


@pytest.fixture
def setup_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    content = "This is the first sentence. This is the second sentence.\nThis is the third sentence. This is the fourth sentence."
    file_path.write_text(content)
    return file_path


def test_read_sentences_from_file_existing_file(setup_file, caplog):
    expected_sentences = ["This is the first sentence", "This is the second sentence", "This is the third sentence",
                          "This is the fourth sentence"]
    caplog.set_level(logging.CRITICAL)

    sentences = read_sentences_from_file(setup_file)
    assert sentences == expected_sentences
    assert f"File '{setup_file}' does not exist." not in caplog.text


def test_read_sentences_from_file_nonexistent_file(caplog):
    non_existing_file = "nonexistent.txt"
    caplog.set_level(logging.CRITICAL)

    sentences = read_sentences_from_file(non_existing_file)
    assert sentences == []
    assert f"File '{non_existing_file}' does not exist." in caplog.text


def test_read_sentences_from_file_empty_file(tmp_path):
    empty_file_path = tmp_path / "empty.txt"
    empty_file_path.touch()

    sentences = read_sentences_from_file(empty_file_path)
    assert sentences == []


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
    game = TypingGame(Level.EASY)
    game.sentences = ["Sentence 1", "Sentence 2", "Sentence 3"]
    game.sentence_iterator = iter(game.sentences)
    game.current_sentence = next(game.sentence_iterator)
    game.user_text = "bla blabla"
    game.total_user_input = ["ha ha ha  ", "bla blabla"]
    game.total_expected_input = ["Sentence 1", "Sentence 2"]

    game.restart_game()

    assert game.current_sentence == game.sentences[0]
    assert game.user_text == ""
    assert game.total_user_input == []
    assert game.total_expected_input == []
