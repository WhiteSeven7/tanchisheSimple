from .data import *


class FreeTail:
    """记录场上的空闲位置，以防苹果生成在苹果上，蛇身上，墙上"""
    def __init__(self, walls, apples, snack_body) -> None:
        # 去除墙后的空闲位置，这是所有可能为空闲的位置
        self.all_tile = [
            (x, y)
            for x in range(0, TILE_WIDTH)
            for y in range(0, TILE_HEIGHT)
            if (x, y) not in walls
        ]
        # 储存apples和snack_body,用于计算空闲位置
        self._apples = apples
        self.snack_body = snack_body


    def get_free_tails(self) -> list[tuple[int, int]]:
        """拿到当前空闲位置"""
        return [
            pos
            for pos in self.all_tile
            if (
                pos not in self.snack_body
                and pos not in (apple.pos for apple in self._apples)
            )
        ]
    
    def reset(self, snack_body):
        self.snack_body = snack_body
