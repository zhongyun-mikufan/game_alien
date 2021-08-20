class Settings:
	"""储存外星人入侵中所有设置的类"""

	def __init__(self):
		"""初始化游戏设置"""
		#屏幕设置
		self.screen_width = 1200
		self.screen_height = 600

		#背景颜色
		self.bg_color = (230,230,230)

		#飞船设置
		self.ship_speed = 1.5

		#子弹设置
		self.bullet_speed = 1.0
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)