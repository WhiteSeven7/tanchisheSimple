import pygame
from ..data import *
from ..menu_obj.button import Button


class MainMenu:
    """
    贪吃蛇街机风
    开始游戏
    """
    def __init__(self, game) -> None:
        self.font = pygame.font.Font(r'res\font\SmileySans-Oblique-3.otf', 75)
        self._init_label()
        self._init_botton(game)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.title_image,self.title_rect)
        self.start_button.draw(surface)


    def _init_label(self):
        self.title_image = self.font.render("贪吃蛇街机风", False, DARK_GREEN)
        self.title_rect = self.title_image.get_rect(center=(WIDTH / 2, GAME_HEIGHT / 4))


    def _init_botton(self, game):
        self.start_button = StartGameButton(game)


    def event_control(self, event: pygame.event.Event)-> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.check_click(event.pos):
                self.start_button.call()


class StartGameButton(Button):
    """主菜单的开始游戏"""
    def __init__(self, game) -> None:
        super().__init__(40, "开始游戏", (WIDTH / 2, GAME_HEIGHT * 3 / 4))
        self._game = game


    def call(self):
        self._game.entry_level()