from gui import Level
from timer import TimerThread
import sys
import editdistance
import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def calculate_accuracy(user_input, expected_input):
    accuracy = 0

    evaluate = editdistance.eval(user_input, expected_input)
    if evaluate > 0:
        accuracy = round((1 - evaluate / len(expected_input)) * 100, 2)

    return accuracy


# def read_sentences_from_file(file_path):
#     sentences_list = []
#     with open(file_path, 'r') as file:
#         text = file.read()
#         sentence_delimiters = ['.', '!', '?']
#         for delimiter in sentence_delimiters:
#             sentences_list.extend(text.split(delimiter))
#         sentences_list = [sentence.strip() for sentence in sentences_list if sentence.strip()]
#     return sentences_list

def read_sentences_from_file(file_path):
    sentences_list = []
    with open(file_path, 'r') as file:
        text = file.read()
        sentence_delimiters = ['.', '!', '?']
        current_sentence = ""
        for char in text:
            current_sentence += char
            if char in sentence_delimiters:
                sentences_list.append(current_sentence.strip())
                current_sentence = ""
    if current_sentence:
        sentences_list.append(current_sentence.strip())
    return sentences_list


def get_text_file_path(difficulty_level):
    match difficulty_level:
        case Level.EASY:
            return './texts/easy.txt'
        case Level.MEDIUM:
            return './texts/medium.txt'
        case Level.HARD:
            return './texts/hard.txt'
        case _:
            return './texts/sample.txt'


class TypingGame:
    def __init__(self, difficulty_level):
        self.running = False
        pygame.init()

        # Set up the screen
        self.WIDTH = 900
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Typing Game")

        # Game variables
        self.font = pygame.font.Font(None, 40)
        self.text_file = get_text_file_path(difficulty_level)
        self.sentences = read_sentences_from_file(self.text_file)
        self.sentence_iterator = None
        self.current_sentence = None
        self.user_text = ""
        self.total_user_input = []
        self.total_expected_input = []

        # Timer variables
        self.timer_thread = TimerThread()

    def display_accuracy(self):
        accuracy = calculate_accuracy(self.total_user_input, self.total_expected_input)
        accuracy_text = self.font.render(f"Accuracy: {accuracy} %", True, WHITE)
        self.screen.blit(accuracy_text, (10, 10))

    def display_user_input(self):
        user_text_render = self.font.render(self.user_text, True, WHITE)
        user_text_rect = user_text_render.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 50))
        self.screen.blit(user_text_render, user_text_rect)

    def display_current_sentence(self):
        sentence_text = self.font.render(self.current_sentence, True, WHITE)
        sentence_rect = sentence_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))
        letter_x = sentence_rect.left  # Starting x-coordinate

        for i, letter in enumerate(self.current_sentence):

            if i < len(self.user_text):
                if self.user_text[i] == letter:
                    letter_color = GREEN  # Green for correct letter
                else:
                    letter_color = RED  # Red for incorrect letter
            else:
                letter_color = WHITE

            letter_surface = self.font.render(letter, True, letter_color)
            letter_rect = letter_surface.get_rect(topleft=(letter_x, sentence_rect.bottom))

            self.screen.blit(letter_surface, letter_rect)

            letter_width = self.font.size(letter)[0]  # Width of the current letter
            letter_x += letter_width  # Update x-coordinate for the next letter

    # def display_current_sentence(self):
    #     sentence_text = self.font.render(self.current_sentence, True, WHITE)
    #     sentence_rect = sentence_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))
    #     max_width = self.WIDTH - 20  # Maximum width to fit within the screen
    #
    #     if sentence_rect.width <= max_width:
    #         # If the sentence fits within the screen width, display it as before
    #         letter_x = sentence_rect.left  # Starting x-coordinate
    #
    #         for i, letter in enumerate(self.current_sentence):
    #             letter_color = WHITE
    #             if i < len(self.user_text):
    #                 if self.user_text[i] == letter:
    #                     letter_color = GREEN  # Green for correct letter
    #                 else:
    #                     letter_color = RED  # Red for incorrect letter
    #
    #             letter_surface = self.font.render(letter, True, letter_color)
    #             letter_rect = letter_surface.get_rect(topleft=(letter_x, sentence_rect.bottom))
    #             self.screen.blit(letter_surface, letter_rect)
    #
    #             letter_width = self.font.size(letter)[0]  # Width of the current letter
    #             letter_x += letter_width  # Update x-coordinate for the next letter
    #     else:
    #         # If the sentence exceeds the screen width, wrap it to multiple lines
    #         words = self.current_sentence.split()
    #         lines = []
    #         current_line = ""
    #         for word in words:
    #             test_line = current_line + word + " "
    #             test_line_render = self.font.render(test_line, True, WHITE)
    #             if test_line_render.get_rect().width > max_width:
    #                 lines.append(current_line.strip())
    #                 current_line = ""
    #             current_line += word + " "
    #
    #         lines.append(current_line.strip())
    #
    #         letter_y = sentence_rect.bottom  # Starting y-coordinate
    #         for line in lines:
    #             line_x = self.WIDTH // 2 - self.font.size(line)[0] // 2  # Starting x-coordinate for each line
    #             for i, letter in enumerate(line):
    #                 letter_color = WHITE
    #                 if i < len(self.user_text):
    #                     if self.user_text[i] == letter:
    #                         letter_color = GREEN  # Green for correct letter
    #                     else:
    #                         letter_color = RED  # Red for incorrect letter
    #
    #                 if i == len(self.user_text) and i < len(
    #                         self.current_sentence):  # Highlight the currently typed letter
    #                     letter_color = WHITE
    #
    #                 letter_surface = self.font.render(letter, True, letter_color)
    #                 letter_rect = letter_surface.get_rect(topleft=(line_x, letter_y))
    #                 self.screen.blit(letter_surface, letter_rect)
    #
    #                 if letter == " ":
    #                     space_width = self.font.size(" ")[0]
    #                     line_x += space_width
    #                 else:
    #                     letter_width = self.font.size(letter)[0]  # Width of the current letter
    #                     line_x += letter_width  # Update x-coordinate for the next letter
    #
    #                 # Increment i by the number of spaces to skip over them
    #                 i += line.count(" ")
    #
    #             letter_y += self.font.get_height()  # Move to the next line

    def next_sentence(self):
        self.total_user_input += self.user_text
        self.total_expected_input += self.current_sentence
        self.current_sentence = next(self.sentence_iterator)
        self.user_text = ""

    def display_restart(self):
        restart_text = self.font.render('RESTART GAME', True, RED)
        restart_rect = restart_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 50))
        self.screen.blit(restart_text, restart_rect)
        return restart_rect

    def restart_game(self):
        self.sentence_iterator = iter(self.sentences)
        self.current_sentence = next(self.sentence_iterator)
        self.user_text = ""
        self.total_user_input = []
        self.total_expected_input = []

        self.start_timer()

    def display_timer(self):
        timer_text = self.font.render(f"Time: {self.timer_thread.remaining_time} s", True, WHITE)
        self.screen.blit(timer_text, (self.WIDTH - 150, 10))

    def start_timer(self):
        if not self.timer_thread.is_alive():
            self.timer_thread = TimerThread()  # Create a new TimerThread object
            self.timer_thread.start()

    def stop_timer(self):
        self.timer_thread.stop()

    def run(self):
        self.running = True
        self.restart_game()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.stop_timer()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.user_text += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    restart_rect = self.display_restart()
                    if restart_rect.collidepoint(event.pos):
                        self.restart_game()

            self.screen.fill(BLACK)

            self.display_current_sentence()
            self.display_user_input()
            self.display_timer()

            if len(self.user_text) == len(self.current_sentence):
                self.next_sentence()

            self.end_game()

            pygame.display.update()

        pygame.quit()

    def end_game(self):
        if not self.timer_thread.is_running:
            self.display_accuracy()
            self.display_restart()

# if __name__ == '__main__':
#     game = TypingGame()
#     game.run()
