import pygame
import random

class SoundSys:
    """处理背景音乐,音效的系统"""
    def __init__(self) -> None:
        self._init_bg()
        # 吃苹果声音
        self.eat_apple = pygame.mixer.Sound(r'res\sound\getScore.wav')
        # 失败声音
        self.fail_sounds = [
            pygame.mixer.Sound(r'res\sound\fail.wav'),
            pygame.mixer.Sound(r'res\sound\fail2.wav')
        ]
        # 创建音效轨道
        self.channel = pygame.mixer.Channel(0)
        # 设置音效轨道音量
        self.channel.set_volume(0.9)

    def _init_bg(self):
        """初始化背景音乐"""
        # 打开音乐文件
        pygame.mixer.music.load(r'res\sound\Funky Stars - Quazar.mp3')
        # 设置音量
        pygame.mixer.music.set_volume(0.5)
        # 循环播放
        pygame.mixer.music.play(-1)

    def set_bg(self, play: bool) -> None:
        """播放/停止背景音乐"""
        if play:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
    
    def play_eat(self) -> None:
        """播放蛇进食音乐"""
        self.channel.play(self.eat_apple)
    
    def play_fail(self) -> None:
        """播放输掉游戏的音乐"""
        sound_effect = random.choice(self.fail_sounds)
        self.channel.play(sound_effect)
