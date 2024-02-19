from collections import deque
import json
import pygame
from pygame.math import Vector2
from ..data import *


class Snack:
    def __init__(self) -> None:
        self.body: deque[Vector2] = self.load_body()
        self.dirction = self.get_dirction(self.body)
        # 现在是否需要张长
        self.grow: bool = False
        # 按照固定的时间运动
        self.time_lock = 0
        self.MOVE_COOL = 300

        # 防止多重转弯bug
        self.used_face = self.dirction


    def draw(self, surface):
        for x, y in self.body:
            rect = pygame.rect.Rect(
                x * TILE_SIZE + (TILE_SIZE - BODY_SIZE) / 2,
                y * TILE_SIZE + (TILE_SIZE - BODY_SIZE) / 2,
                BODY_SIZE,
                BODY_SIZE
            )
            pygame.draw.rect(surface, DARK_GREEN, rect, border_radius=5)


    def control(self, keys: list[bool]):
        # 左
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.used_face is not RIGHT:
            self.dirction = LEFT
        # 右
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.used_face is not LEFT:
            self.dirction = RIGHT
        # 上
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.used_face is not DOWN:
            self.dirction = UP
        # 下
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.used_face is not UP:
            self.dirction = DOWN


    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time_lock > self.MOVE_COOL:
            self.move()
            self.transmit()
            self.time_lock = current_time


    def move(self):
        """移动,并非每帧调用"""
        if self.grow:
            self.grow = False
        else:
            self.body.pop()
        new_pos: Vector2 = self.dirction + self.body[0]
        self.body.appendleft(new_pos)
        # 更新"用过的方向"
        self.used_face = self.dirction


    def reset(self):
        self.__init__()


    def transmit(self):
        """让蛇在越过边界时传送到另一侧"""
        head: Vector2 = self.body[0]
        # x轴
        if head.x >= TILE_WIDTH:
            head.x -= TILE_WIDTH
        elif head.x < 0:
            head.x += TILE_WIDTH
        # y轴
        if head.y >= TILE_HEIGHT:
            head.y -= TILE_HEIGHT
        elif head.y < 0:
            head.y += TILE_HEIGHT
        

    @staticmethod
    def load_body() -> deque[Vector2]:
        with open(r'res\user_data\map.json', mode='r') as file:
            map_data = json.load(file)
        # {1: Vector2(x1, y1), 2: Vector2(x2, y2), ...}
        body_dict = {
            i: Vector2(x, y)
            for y, row in enumerate(map_data)
            for x, i in enumerate(row)
            if i > 0
        }
        return deque(
            body_dict[sorted_key]
            for sorted_key in sorted(body_dict)
        )


    @staticmethod
    def get_dirction(body: deque[Vector2]) -> Vector2:
        direction = body[0] - body[1]
        for dir in DIRECTIONS:
            if dir == direction:
                return dir
