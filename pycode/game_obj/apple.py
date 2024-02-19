import random
import pygame
from ..data import *
from ..free_tail import FreeTail


class Apple(pygame.sprite.Sprite):
    def __init__(self, image_sys: "AppleSys", pos: tuple[int, int]) -> None:
        super().__init__()
        self._image_sys = image_sys
        self.hp = 600 - 1
        self.pos = pos
        self._inir_image_rect()

    def _inir_image_rect(self):
        self.image = self._image_sys.images[self.hp // 200]
        self.rect = pygame.rect.Rect(
            self.pos[0] * TILE_SIZE + (TILE_SIZE - APPLE_SIZE) / 2,
            self.pos[1] * TILE_SIZE + (TILE_SIZE - APPLE_SIZE) / 2,
            APPLE_SIZE,
            APPLE_SIZE
        )

    
    def set_image(self):
        """根据hp设置自己的正确的图像"""
        self.image = self._image_sys.images[self.hp // 200]


    def set_kill(self):
        """一段时间后自己消失"""
        if self.hp == 0:
            self.kill()

    def update(self) -> None:
        self.hp -= 1
        self.set_image()
        self.set_kill()

    def energy(self):
        """公开接口,得到现在这个苹果的给多少分"""
        return self.hp // 200 + 1
        

class AppleSys(pygame.sprite.Group):
    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)
        # 所有苹果的图像
        self.images  = [
            pygame.image.load('res/image/1.png').convert_alpha(),
            pygame.image.load('res/image/2.png').convert_alpha(),
            pygame.image.load('res/image/3.png').convert_alpha()
        ]
        self.lock_time = 0
        # 生成苹果的间隔,单位毫秒. 不是直接生成,而是会有计算
        self.APPLE_COOL = 2400


    def set_free_tail(self, free_tail: FreeTail):
        self._free_tail = free_tail
    

    def add_apple(self):
        """添加苹果"""
        free_tile = random.choice(self._free_tail.get_free_tails())
        self.add(Apple(self, free_tile))
        self.lock_time = pygame.time.get_ticks()


    def update(self, *args, **kwargs) -> None:
        """
        苹果数量0,立刻生成
        苹果数量大于等于5,不生成
        苹果数量n,每COOL时间,有 1/(5*n+1)概率生成
        """
        num = len(self)
        if (
            num == 0 or (
                num < 5 
                and pygame.time.get_ticks() - self.lock_time > self.APPLE_COOL 
                and not random.randint(0, 5 * num)
            )
        ):
            self.add_apple()
        return super().update(*args, **kwargs)


    def reset(self):
        self.empty()
