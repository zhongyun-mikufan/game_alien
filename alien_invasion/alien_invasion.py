#使用sys的工具退出游戏
import sys

#包含开发游戏需要的功能
import pygame

#加载飞船图像
from ship import Ship

#加载子弹
from bullet import Bullet


from settings import Settings

class AlienInvasion:
    """Overall总体的 class to manage game assets（游戏资源） and behavior."""

    def __init__(self):
        """Initialize初始化 the game, and create game resources资源."""
        pygame.init()

        self.settings = Settings()

        # #全屏游戏的代码（暂时不用）
        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        #根据设置自定义窗口大小
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        #caption说明
        pygame.display.set_caption("AlienInvasion")

        self.ship = Ship(self)
        # 储存子弹的编组
        self.bullets = pygame.sprite.Group()

    def _check_events(self):
        """响应案件和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                #摁键方法
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                #摁键松开方法
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按键摁下"""
        if event.key == pygame.K_RIGHT:
            #向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            #向右移动飞船
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应按键松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创造一颗子弹，并将其加入编组bullets中"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        # Redraw the screen 重绘屏幕during each pass through the loop.
        #设置背景颜色
        self.screen.fill(self.settings.bg_color)

        #在指定位置绘制飞船
        self.ship.blitme()

        # 更新子弹图像
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            self.ship.update()
            # 子弹的循环
            self.bullets.update()
            # 重构代码很重要，看起来更简介
            self._update_screen()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
