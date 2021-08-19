import sys
#使用sys的工具退出游戏

import pygame
#包含开发游戏需要的功能

from ship import Ship
#加载飞船图像

from settings import Settings

class AlienInvasion:
    """Overall总体的 class to manage game assets（游戏资源） and behavior."""

    def __init__(self):
        """Initialize初始化 the game, and create game resources资源."""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        #caption说明
        pygame.display.set_caption("AlienInvasion")

        self.ship = Ship(self)



    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw the screen 重绘屏幕during each pass through the loop.
            #设置背景颜色
            self.screen.fill(self.settings.bg_color)

            #在指定位置绘制飞船
            self.ship.blitme()

            # Make the most recently drawn screen visible.
            pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
