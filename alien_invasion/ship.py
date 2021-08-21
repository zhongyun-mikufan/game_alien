import pygame

class Ship():
	"""管理飞船的类"""
	def __init__(self, ai_game):
		"""初始化飞船并设置其初始位置"""
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()
		#rectify 矫正

		#加载飞船图像获取其外界矩形。
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()

		#对于每艘新飞船都将其放在屏幕底部中央
		self.rect.midbottom = self.screen_rect.midbottom

		#在飞船属性x中储存小数值
		self.x = float(self.rect.x)

		# 移动标志
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""根据移动标志调整飞船位置"""
		#更新飞船而不是rect对象的x值
		#self.rect.right 返回飞船外接矩形右边缘的x坐标
		if self.moving_right and (self.rect.right < self.screen_rect.right):
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		# 根据self.x更新rect对象
		self.rect.x = self.x

	def blitme(self):
		"""在指定位置绘制飞船"""
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""让飞船在屏幕底部居中"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
