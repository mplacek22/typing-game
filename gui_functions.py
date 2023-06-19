import pygame


def draw_heading(screen, typed_text):
    font_title = pygame.font.Font(None, 60)
    text = font_title.render(typed_text, True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, 150))
    screen.blit(text, text_rect)


def draw_button(screen, text, color, used_button):
    font_button = pygame.font.Font(None, 40)
    pygame.draw.rect(screen, color, used_button)
    button_text = font_button.render(text, True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=used_button.center)
    screen.blit(button_text, button_text_rect)
