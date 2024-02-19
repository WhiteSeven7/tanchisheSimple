import pygame
from ..data import *


class PauseMenu:
    """
    游戏暂停
    <- 继续   主菜单 -> 
    """
    def __init__(self, level, game) -> None:
        self.font = pygame.font.Font(r"res\font\SmileySans-Oblique-3.otf", 75)
        self.small_font = pygame.font.Font(r"res\font\SmileySans-Oblique-3.otf", 45)
        self._init_image_rect()

        self._level = level
        self._game = game


    def draw(self, surface: pygame.Surface):
        surface.blits(self.image_rect_list)


    def _init_image_rect(self) -> None:
        images = [
            self.font.render("游戏暂停", True, DARK_GREEN),
            self.small_font.render("<- 继续", True, DARK_GREEN),
            self.small_font.render("主菜单 ->", True, DARK_GREEN),
        ]
        rects = [
            images[0].get_rect(center=(WIDTH / 2, GAME_HEIGHT / 4)),
            images[1].get_rect(center=(WIDTH / 4, GAME_HEIGHT * 3 / 4)),
            images[2].get_rect(center=(WIDTH * 3 / 4, GAME_HEIGHT * 3 / 4)),
        ]
        self.image_rect_list = list(zip(images, rects))

    
    def event_key_control(self, key: int)-> None:
        """处理 <- 和 -> """
        if key in (pygame.K_LEFT, pygame.K_a):
            self._level.set_pause(False)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self._game.quit_level()
        