# 使用sys的工具退出游戏
import sys

# 包含开发游戏需要的功能
import pygame

# 从模块time中加载暂停功能
from time import sleep

# 加载飞船图像
from ship import Ship

# 加载外星人
from alien import Alien

# 加载统计数据,得分
from game_stats import Gamestats
from scoreboard import Scoreboard

# 加载子弹
from bullet import Bullet

# 加载按钮
from button import Button

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

        # 根据设置自定义窗口大小
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # caption说明
        pygame.display.set_caption("AlienInvasion")

        # 用于统计信息的实例和记分牌
        self.stats = Gamestats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        # 储存子弹的编组
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 创建Play按钮
        self.play_button = Button(self, "Play")

    def _check_events(self):
        """响应案件和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # 摁键方法
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                # 摁键松开方法
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏设置
            self.settings.initialize_dynamic_settings()

            # 重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()

            # 清空屏幕外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏光标
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """响应按键摁下"""
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 向右移动飞船
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
        # 检查子弹是否小于上限
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除子弹"""
        # 更新子弹位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # 显示子弹数字（注意：将输出写入终端的时间比
        #   将图形绘制到游戏窗口花费的事件还要多）
        # print(len(self.bullets))

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """响应外星人和子弹碰撞"""
        # 检查是否有子弹击中外星人
        # 是就删除二者
        # 第一个布尔实参Ture改为False的话子弹不会消失
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.aliens:
            # 删除现有的子弹，生成新的外星人,增加游戏速度
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _ship_hit(self):
        """响应飞船被外星人碰撞"""
        if self.stats.ships_left > 0:
            # 船数量减一
            self.stats.ships_left -= 1

            # 清空屏幕的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创造新的外星人，把船放在屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(1)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_alien_bottom(self):
        """检查是否有飞船触底"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被碰到一样处理
                self._ship_hit()
                break

    def _update_aliens(self):
        """
        检查是否有外星人处于屏幕边缘
        更新外星人群中所有外星人的位置
        """
        self._check_fleet_edges()
        self.aliens.update()

        # 检查外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print("YOU ARE DEAD")

        # 检查外星人是否到达底部
        self._check_alien_bottom()

    def _update_screen(self):
        # Redraw the screen 重绘屏幕during each pass through the loop.
        # 设置背景颜色
        self.screen.fill(self.settings.bg_color)

        # 在指定位置绘制飞船
        self.ship.blitme()

        # 更新子弹图像
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并计算一行可以容纳多少外星人
        # 外星人的间距为外星人的宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avaliable_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = avaliable_space_x // (2 * alien_width)

        # 计算屏幕可容纳多少外星人
        ship_height = self.ship.rect.height
        avaliable_space_y = (self.settings.screen_height -
            (3 * alien_height) - ship_height)

        number_rows = avaliable_space_y // (2 * alien_height)

        # 创造第一行外星人
        for row_number in range (number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创造一个外星人并将其加入当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """有外星人达到边缘时响应相对措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变他们方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                # 子弹的循环
                self._update_bullets()
                # 重构代码很重要，看起来更简洁

                # 更新外星人位置
                self._update_aliens()

            self._update_screen()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
