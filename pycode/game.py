import json
import sys
from abc import ABC, abstractmethod
from itertools import islice
import pygame
from .data import *
from .game_obj.snack import Snack
from .game_obj.apple import AppleSys, Apple
from .game_obj.wall import WallSys
from .info import Info
from .menu.fail_menu import FailMenu
from .menu.pause_menu import PauseMenu
from .sound_sys import SoundSys
from .free_tail import FreeTail


class BaseGame(ABC):
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.surface = pygame.display.set_mode(SIZE)
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
        self.score = 0
        # 影响控制和update
        self.fail = False

        self.snack = Snack()
        self.apple_sys = AppleSys()
        self.wall_sys = WallSys()

        self.info = Info(self.max_score)
        self.fail_menu = FailMenu()
        self.sound_sys = SoundSys()
        # 用于在生成苹果时，拿到空位置
        self.free_tail = FreeTail(self.wall_sys, self.apple_sys, self.snack.body)

        self.apple_sys.set_free_tail(self.free_tail)
        # 暂停游戏
        self.pause = False
        self.pause_menu = PauseMenu()


    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
                continue
            elif event.type == pygame.KEYDOWN:
                if self.fail:
                    if event.key == pygame.K_SPACE:
                    # 输的状态重启游戏
                        self.reset()
                elif event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                    self.set_pause(not self.pause)
        if not self.fail:
            keys = pygame.key.get_pressed()
            self.snack.control(keys)


    def snack_eat_apple(self):
        apple: Apple
        for apple in self.apple_sys:
            if apple.pos == self.snack.body[0]:
                # 让蛇张长
                self.snack.grow = True
                # 得分增加
                self.score += apple.energy()
                self.do_when_change_score()
                # 播放吃食物的音效
                self.sound_sys.play_eat()
                # 清除被吃掉的苹果
                apple.kill()

    
    def do_when_change_score(self):
        """分数改变时时调用"""
        if self.score > self.max_score:
            self.max_score = self.score
            self.info.update_score(self.score, self.max_score)
        else:
            self.info.update_score(self.score)


    def snack_hit_wall_snack_and_border(self):
        """检查碰撞,撞了会输掉"""
        # pygame.Vector2可以和tuple比较是否相等
        head: pygame.Vector2 = self.snack.body[0]
        # 撞自己
        for body in islice(self.snack.body, 1, None):
            if body == head:
                self.set_fail()
                return
        # 撞墙
        for wall_pos in self.wall_sys:
            if wall_pos == head:
                self.set_fail()
                return
        # # 撞边界
        # if not(0 <= head[0] < TILE_WIDTH and 0 <= head[1] < TILE_HEIGHT):
        #     self.set_fail()
        #     return
        

    def update(self):
        if self.fail or self.pause:
            return
        # 苹果先更新
        self.apple_sys.update()
        # 蛇再更新
        self.snack.update()
        # 蛇吃苹果
        self.snack_eat_apple()
        # 蛇撞东西
        self.snack_hit_wall_snack_and_border()


    def draw(self):
        # 背景颜色
        self.surface.fill(LIGHT_GREEN)
        # 游戏和底部分数的分界线
        pygame.draw.line(self.surface, DARK_GREEN, (0, GAME_HEIGHT + 3), (WIDTH, GAME_HEIGHT + 3), 6)
        if self.fail:
            self.fail_menu.draw(self.surface)
        elif self.pause:
            self.pause_menu.draw(self.surface)
        else:
            self.snack.draw(self.surface)
            self.apple_sys.draw(self.surface)
            self.wall_sys.draw(self.surface)
        self.info.draw(self.surface)
        # 更新画面 flip
        super().draw()


    def reset(self):
        """重启游戏"""
        self.fail = False
        self.score = 0
        self.snack.reset()
        self.apple_sys.reset()
        self.sound_sys.set_bg(True)
        # free_tail重置
        self.free_tail.reset(self.snack.body)
        # 得分重置
        self.info.reset()


    def safe_quit(self):
        self.save_data()
        return super().safe_quit()
    

    def set_fail(self):
        """在玩家输掉时调用"""
        self.fail = True
        self.fail_menu.reset(self.score, self.max_score)
        self.sound_sys.play_fail()
        self.sound_sys.set_bg(False)

    
    def set_pause(self, pause):
        """暂停时调用"""
        self.pause = pause
        self.sound_sys.set_bg(not pause)

