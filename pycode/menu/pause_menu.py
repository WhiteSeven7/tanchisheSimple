import pygame
from ..data import *


class PauseMenu:
    """游戏暂停"""
    def __init__(self) -> None:
        self.font = pygame.font.Font(r"res\font\SmileySans-Oblique-3.otf", 75)
        self.text_image = self.font.render("游戏暂停", False, DARK_GREEN)
        self.rect = self.text_image.get_rect(center=(WIDTH / 2, GAME_HEIGHT / 2))


    def draw(self, surface: pygame.Surface):
        surface.blit(self.text_image, self.rect)

