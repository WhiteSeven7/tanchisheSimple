import json
import pygame.draw
from ..data import *

class WallSys:
    @staticmethod
    def get_walls() -> list[tuple[int, int]]:
        """从文件读取墙的设置"""
        with open(r'res\user_data\map.json', mode='r') as file:
            map = json.load(file)
        return [
            (x, y)
            for y, row in enumerate(map)
            for x, i in enumerate(row)
            if i == -1
        ]


    def __init__(self) -> None:
        # 这个wall的数据类型是位置
        self.walls: list[tuple[int, int]] = self.get_walls()
        self.wall_rects: list[pygame.Rect] = [
            pygame.rect.Rect(
                x * TILE_SIZE,
                y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
            for x, y in self.walls
        ]
    

    def __iter__(self):
        return iter(self.walls)


    def draw(self, surface) -> None:
        for wall_rect in self.wall_rects:
            pygame.draw.rect(surface, DARK_GREEN, wall_rect)
