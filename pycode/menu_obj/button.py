from abc import ABC, abstractmethod
import pygame
from ..data import *


class Button(ABC):
    """基础的按钮"""
    def __init__(self, size: int, text: str, pos: tuple[int, int]) -> None:
        self.font = pygame.font.Font(r'res\font\SmileySans-Oblique-3.otf', size)
        self._set_image_rect(text, pos)

    def _set_image_rect(self, text: str, pos: tuple[int, int]):
        border = 6
        text_image = self.font.render(text, False, DARK_GREEN, LIGHT_GREEN)
        self.rect = text_image.get_rect(center=pos).inflate(2 * border, 2 * border)
        self.image = pygame.Surface(self.rect.size)
        self.image.blit(text_image, (border, border))

    
    def draw(self, surface: pygame.Surface)-> None:
        surface.blit(self.image, self.rect)


    @abstractmethod
    def call(self):
        ...

    
    def check_click(self, pos: tuple[int, int]):
        return self.rect.collidepoint(pos)
