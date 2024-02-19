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


class Level:
    def __init__(self, game, sound_sys: SoundSys) -> None:
        self._game = game
        self.score = 0
        # 影响控制和update
        self.fail = False

        self.snack = Snack()
        self.apple_sys = AppleSys()
        self.wall_sys = WallSys()

        self.info = Info(self._game.max_score)
        self.fail_menu = FailMenu()
        # 用于在生成苹果时，拿到空位置
        self.free_tail = FreeTail(self.wall_sys, self.apple_sys, self.snack.body)

        self.apple_sys.set_free_tail(self.free_tail)
        # 暂停游戏
        self.pause = False
        self.pause_menu = PauseMenu()
        # 声音管理系统
        self.sound_sys = sound_sys


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
        if self.score > self._game.max_score:
            self._game.max_score = self.score
            self.info.update_score(self.score, self._game.max_score)
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


    def draw(self, surface: pygame.Surface):
        if self.fail:
            # 输的时候
            self.fail_menu.draw(surface)
        elif self.pause:
            # 暂停
            self.pause_menu.draw(surface)
        else:
            # 正常游戏
            self.snack.draw(surface)
            self.apple_sys.draw(surface)
            self.wall_sys.draw(surface)
        self.info.draw(surface)

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
    

    def set_fail(self):
        """在玩家输掉时调用"""
        self.fail = True
        self.fail_menu.reset(self.score, self._game.max_score)
        self.sound_sys.play_fail()
        self.sound_sys.set_bg(False)

    
    def set_pause(self, pause):
        """暂停时调用"""
        self.pause = pause
        self.sound_sys.set_bg(not pause)


    def event_control(self, event: pygame.event.Event)-> None:
        """处理单个event事件"""
        if event.type == pygame.KEYDOWN:
            if self.fail:
                if event.key == pygame.K_SPACE:
                # 输的状态重启游戏
                    self.reset()
            elif event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                self.set_pause(not self.pause)

    
    def keys_control(self, keys: list[bool])-> None:
        """处理按键状态"""
        if not self.fail:
            keys = pygame.key.get_pressed()
            self.snack.control(keys)


    def need_keys(self)-> None:
        """检测自己需不需要keys"""
        return not (self.fail or self.pause)
