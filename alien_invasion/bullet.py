import pygame
from pygame.sprite import Sprite

class Bulleg(Sprite):
	"""管理飞船所发子弹的类"""

	def __init__(self, ai_game):
		"""在飞船前创造一个子弹对象"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color\

		# 在(0,0)创建一个表示子弹的举行，再设置正确的位置。
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
			self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop

		$储存用小数表示的子弹位置
		self.y = float(self.rect.y)
		