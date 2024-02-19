import pygame
from ..data import *


class FailMenu:
    def __init__(self) -> None:
        """
        你 输 了
        本次得分：，最高分：
        按空格键重开游戏
        """
        self.font = pygame.font.Font(r'res\font\SmileySans-Oblique-3.otf', 60)
        self.small_font = pygame.font.Font(r'res\font\SmileySans-Oblique-3.otf', 40)
        self.text_images: list[pygame.Surface] = [
            self.font.render('你输了',False, DARK_GREEN),
            self.font.render(f'本次得分：{1}，最高分：{1}',False, DARK_GREEN),
            self.small_font.render('按任意空格键重开游戏',False, DARK_GREEN)
        ]
        # 位置x轴居中,y轴三等分居中
        self.pos_list = [
            (
                (WIDTH - text_image.get_width()) / 2,
                (GAME_HEIGHT * (2 * index + 1) / 6 - text_image.get_height() / 2)
            )
            for index, text_image in enumerate(self.text_images)
        ]

    def reset(self, score: int, max_score: int):
        """在重新开始游戏时调用"""
        self.text_images[1] = self.font.render(f'本次得分：{score}，最高分：{max_score}',False, DARK_GREEN)
        self.pos_list[1] = (
            (WIDTH - self.text_images[1].get_width()) / 2,
            (GAME_HEIGHT - self.text_images[1].get_height()) / 2
        )

    def draw(self, surface: pygame.Surface):
        surface.blits(zip(self.text_images, self.pos_list))
