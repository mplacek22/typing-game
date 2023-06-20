import logging
import os
import re
import editdistance
import pygame
from game_logic.colors import WHITE
from game_logic.difficulty_level import Level


def draw_heading(screen, typed_text):
    font_title = pygame.font.Font(None, 60)
    text = font_title.render(typed_text, True, WHITE)
    text_rect = text.get_rect(center=(screen.get_width() // 2, 150))
    screen.blit(text, text_rect)


def draw_button(screen, text, color, used_button):
    font_button = pygame.font.Font(None, 40)
    pygame.draw.rect(screen, color, used_button)
    button_text = font_button.render(text, True, WHITE)
    button_text_rect = button_text.get_rect(center=used_button.center)
    screen.blit(button_text, button_text_rect)


def calculate_accuracy(user_input, expected_input):
    if len(expected_input) == 0:
        raise ZeroDivisionError

    if len(user_input) != len(expected_input):
        raise ValueError(f"Input lengths do not match {len(user_input)}, {len(expected_input)}")

    return round((1 - editdistance.eval(user_input, expected_input) / len(expected_input)) * 100, 2)


def read_sentences_from_file(file_path):
    logger = logging.getLogger(__name__)

    try:
        with open(file_path, 'r') as file:
            text = file.read()
            sentence_delimiters = r'[.!?]+[\n\s]*'
            sentences_list = re.split(sentence_delimiters, text)
            sentences_list = [sentence.strip() for sentence in sentences_list if sentence.strip()]
        return sentences_list
    except FileNotFoundError:
        logger.critical(f"File '{file_path}' does not exist.")
        return []


def get_text_file_path(difficulty_level):
    parent_dir = get_parent_dir()
    file_paths = {
        Level.EASY: os.path.join(parent_dir, 'texts/easy.txt'),
        Level.MEDIUM: os.path.join(parent_dir, 'texts/medium.txt'),
        Level.HARD: os.path.join(parent_dir, 'texts/hard.txt'),
    }
    return file_paths.get(difficulty_level)


def get_parent_dir():
    current_dir = os.getcwd()  # Store the current directory
    os.chdir('..')  # Change to the parent directory
    parent_dir = os.getcwd()  # Get the new current directory
    os.chdir(current_dir)  # Change back to the original directory
    return parent_dir


