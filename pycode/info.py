import pygame
from .data import *

class Info(pygame.sprite.Sprite):
    "得分：{}      最高分：{}"
    def __init__(self, max_score) -> None:
        self.font = pygame.font.Font(r'res\font\SmileySans-Oblique-3.otf', 60)
        self._set_score(0)
        self._set_max_score(max_score)


    def update_score(self, score, max_score=None):
        """更新得分与最高得分,对外接口"""
        self._set_score(score)
        self._set_max_score(max_score)


    def reset(self):
        """重置得分"""
        self._set_score(0)


    def draw(self, surface: pygame.Surface):
        surface.blit(self.score_image, self.pos)
        surface.blit(self.max_image, self.ms_pos)

    
    def _set_score(self, score):
        """设置 得分"""
        self.score_image: pygame.Surface = self.font.render(f'得分：{score}', False, DARK_GREEN)
        self.pos = self.score_image.get_rect(midleft=(20, GAME_HEIGHT + SCORE_HEIGHT / 2))


    def _set_max_score(self, max_score=None):
        """设置 最高得分"""
        if max_score is not None:
            self.max_image: pygame.Surface = self.font.render(f'最高分：{max_score}', False, DARK_GREEN)
            self.ms_pos = self.max_image.get_rect(midright=(WIDTH - 20, GAME_HEIGHT + SCORE_HEIGHT / 2))
