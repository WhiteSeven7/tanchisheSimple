from abc import ABC, abstractmethod
import pygame
from ..data import *


class Button(ABC):
    """基础的按钮"""
    def __init__(self, size: int, text: str, pos: tuple[int, int]) -> None:
        self.font = pygame.font.Font(r'res\font\SmileySans-Oblique-3.otf', size)
        self._set_image_rect(text, pos)

    def _set_image_rect(self, text: str, pos: tuple[int, int]):
        # 内边距
        padding = 6
        # 边框宽度
        border = 6
        text_image = self.font.render(text, True, DARK_GREEN)
        self.rect = (
            text_image.get_rect(center=pos)
            .inflate(2 * (border + padding), 2 * (border + padding))
        )
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(LIGHT_GREEN)
        pygame.draw.rect(self.image, DARK_GREEN, ((0, 0), self.rect.size), border)
        self.image.blit(text_image, (border + padding, border + padding))

    
    def draw(self, surface: pygame.Surface)-> None:
        surface.blit(self.image, self.rect)


    @abstractmethod
    def call(self):
        ...

    
    def check_click(self, pos: tuple[int, int]):
        return self.rect.collidepoint(pos)
