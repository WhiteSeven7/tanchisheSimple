import pygame
from ..data import *


class FailMenu:
    def __init__(self, level, game) -> None:
        """
        你 输 了
        本次得分：{}，最高分：{}
        <- 重开     主菜单 ->
        """
        self.big_font = pygame.font.Font(r'res\font\SmileySans-Oblique-3.otf', 80)
        self.font = pygame.font.Font(r'res\font\SmileySans-Oblique-3.otf', 55)
        # self.small_font = pygame.font.Font(r'res\font\SmileySans-Oblique-3.otf', 30)
        self._init_image_rect()

        self._level = level
        self._game = game


    def reset(self, score: int, max_score: int):
        """在重新开始游戏时调用"""
        image: pygame.Surface = self.font.render(f'本次得分：{score}，最高分：{max_score}',True, DARK_GREEN)
        rect: pygame.Rect = image.get_rect(center=(WIDTH / 2, GAME_HEIGHT / 2))
        self.image_rect_list[1] = image, rect


    def draw(self, surface: pygame.Surface):
        surface.blits(self.image_rect_list)


    def _init_image_rect(self) -> None:
        images: list[pygame.Surface] = [
            self.big_font.render('你输了',True, DARK_GREEN),
            self.font.render(f'本次得分：{1}，最高分：{1}',True, DARK_GREEN),
            self.font.render('<- 重开',True, DARK_GREEN),
            self.font.render('主菜单 ->',True, DARK_GREEN),
        ]
        rects: list[pygame.Rect] = [
            images[0].get_rect(center=(WIDTH / 2, GAME_HEIGHT / 6)),
            images[1].get_rect(center=(WIDTH / 2, GAME_HEIGHT / 2)),
            images[2].get_rect(center=(WIDTH / 4, GAME_HEIGHT * 5 / 6)),
            images[3].get_rect(center=(WIDTH * 3 / 4, GAME_HEIGHT * 5 / 6)),
        ]
        self.image_rect_list = list(zip(images, rects))

    
    def event_key_control(self, key: int) -> None:
        """处理 <- 和 -> """
        if key in (pygame.K_LEFT, pygame.K_a):
            self._level.reset()
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self._game.quit_level()
        