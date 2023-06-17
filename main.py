import random
import sys
import time

import pygame

background_image = 'images/background.jpg'
sentences_file = 'texts/lorem_ipsum.txt'
restart_logo = 'restart.png'


class Type_Game:
    def __init__(self):
        self.color_heading = (49, 58, 82)
        self.color_text = (235, 230, 232)
        self.color_results = (216, 222, 146)
        self.w = 750
        self.h = 550
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.active = False
        self.results = "Time:0 ~ Accuracy:0 % ~ Words Per Minute:0"
        self.accuracy = "0%"
        self.reset = True
        pygame.init()
        pygame.display.set_caption("Typing Game")
        self.bg_img = pygame.image.load(background_image)
        self.bg_img = pygame.transform.scale(self.bg_img, (750, 550))

    def write_text(self, screen, title, y, f_size, text_color):
        font_family = pygame.font.SysFont(None, f_size)
        text = font_family.render(title, 1, text_color)
        text_box = text.get_rect(center=(self.w / 2, y))
        screen.blit(text, text_box)
        pygame.display.update()

    def show_result(self, screen):
        if not self.end:
            self.total_time = time.time() - self.start_time
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count = count + 1
                except:
                    pass
            self.accuracy = (count * 100) / len(self.word)
        self.wpm = (len(self.input_text) * 60) / (5 * self.total_time)
        self.end = True
        self.results = "Time: " + str(round(self.total_time)) + " secs ~ Accuracy: " + str(
            round(self.accuracy)) + "% ~ WPM: " + str(round(self.wpm))
        self.reply_img = pygame.image.load(restart_logo)
        self.reply_img = pygame.transform.scale(self.reply_img, (200, 100))
        screen.blit(self.reply_img, (self.w / 2 - 70, self.h - 130))
        pygame.display.update()

    def get_sentence(self):
        return random.choice(open(sentences_file).read().split('\n'))

    def restart_game(self):
        time.sleep(1)
        self.reset = False
        self.end = False
        self.input_text = ''
        self.word = ''
        self.start_time = 0
        self.total_time = 0
        self.wpm = 0
        self.word = self.get_sentence()
        if (not self.word): self.restart_game()
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg_img, (0, 0))
        title = "Typing Game"
        self.write_text(self.screen, title, 80, 72, self.color_heading)
        pygame.draw.rect(self.screen, (255, 190, 20), (50, 200, 700, 50), 2)
        self.write_text(self.screen, self.word, 200, 24, self.color_text)
        pygame.display.update()

    def run(self):
        self.restart_game()
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            pygame.draw.rect(self.screen, self.color_heading, (50, 200, 700, 50), 3)
            self.write_text(self.screen, self.input_text, 274, 24, (250, 250, 250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if 50 <= x <= 700 and 200 <= y <= 300:
                        self.active = True
                        self.input_text = ''
                        self.start_time = time.time()
                    elif 310 <= x <= 510 and 390 <= y <= 500 and self.end:
                        self.restart_game()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_result(self.screen)
                            print(self.results)
                            self.write_text(self.screen, self.results, 350, 28, self.color_results)
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    Type_Game().run()
