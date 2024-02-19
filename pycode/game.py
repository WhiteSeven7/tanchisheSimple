import json
import sys
from abc import ABC, abstractmethod
from typing import Callable
import pygame
from .data import *
from .level import Level
from .menu.main_menu import MainMenu
from .sound_sys import SoundSys

class BaseGame(ABC):
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.surface = pygame.display.set_mode(SIZE)
        pygame.display.set_icon(pygame.image.load(r'res\image\1.png'))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("贪吃蛇街机风")
        self.quit = False


    @abstractmethod
    def control(self):
        ...


    @abstractmethod
    def update(self):
        ...


    @abstractmethod
    def draw(self):
        pygame.display.flip()


    def run(self):
        while not self.quit:
            self.control()
            self.update()
            self.draw()
            self.clock.tick(60)
        self.safe_quit()


    def safe_quit(self):
        pygame.mixer.quit()
        pygame.font.quit()
        pygame.quit()
        sys.exit()


class Game(BaseGame):
    @staticmethod
    def load_data():
        """载入最高分"""
        with open('res/user_data/max_score.json', mode='r') as file:
            return json.load(file)


    def save_data(self):
        """储存最高分"""
        with open('res/user_data/max_score.json', mode='w') as file:
            json.dump(self.max_score, file)


    def __init__(self) -> None:
        super().__init__()
        self.max_score = self.load_data()
        # 是在游戏还是菜单
        self.level_running = False
        # 声音管理
        self.sound_sys = SoundSys()
        self.sound_sys.set_bg(self.level_running)

        self.level = Level(self, self.sound_sys)
        self.main_menu = MainMenu(self)

    def control(self):
        event_control: Callable[[pygame.event.Event], None] = (
            self.level.event_control
            if self.level_running
            else self.main_menu.event_control
        )
        event: pygame.event.Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
                continue
            event_control(event)
        if self.level_running and self.level.need_keys():
            keys: list[bool] = pygame.key.get_pressed()
            self.level.keys_control(keys)


    def draw(self):
        # 背景颜色
        self.surface.fill(LIGHT_GREEN)
        # 游戏和底部分数的分界线
        pygame.draw.line(self.surface, DARK_GREEN, (0, GAME_HEIGHT + 3), (WIDTH, GAME_HEIGHT + 3), 7)
        if self.level_running:
            # 游戏运行时,绘制
            self.level.draw(self.surface)
        else:
            self.main_menu.draw(self.surface)
        # 更新画面 flip
        super().draw()


    def safe_quit(self):
        self.save_data()
        return super().safe_quit()


    def update(self):
        if self.level_running:
            self.level.update()
        return super().update()
    

    def entry_level(self):
        """开始游戏"""
        self.level_running = True
        self.level.reset()

    
    def quit_level(self):
        self.level_running = False
