'''
Function:
	定义一些精灵类
'''
import pygame
import random


YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


'''墙类'''
class Wall(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, color, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y


'''食物类'''
class Food(pygame.sprite.Sprite):
	magic_list = [
		'', '', '', '', '',
		'', '', '', '', '',
		'', '', '', '', '',
		'', '', '', '', '',
		'', '', '', '', '',
		'', '', '', '', '',
		'', '', '', '', '',
		'', '', '', '', '',
		'', '', '', '', '',
		'score', 'strong', 'view'
	]

	def __init__(self, x, y):
		width, height = 6, 6
		color = YELLOW
		self.magic = random.choice(self.magic_list)
		if self.magic == 'score':
			width, height = 12, 12
			x -= 3
			y -= 3
		elif self.magic == 'strong':
			color = RED
		elif self.magic == 'view':
			color = GREEN

		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height]).convert_alpha()
		self.image.fill("#00000000")
		pygame.draw.ellipse(self.image, color, [0, 0, width, height])
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y




'''角色类'''
class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, role_image_path, is_move=False, tracks=None):
		pygame.sprite.Sprite.__init__(self)
		self.role_name_path = role_image_path
		self.base_image = pygame.image.load(role_image_path).convert_alpha()
		self.image = self.base_image.copy()
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y
		self.prev_x = x
		self.prev_y = y
		self.base_speed = [30, 30]
		self.speed = [0, 0]
		self.is_move = is_move
		self.tracks = [] if tracks is None else tracks
		self.tracks_loc = [0, 0]

		self.weak = False

	'''特殊变色'''
	def change_image(self):
		changed_image = pygame.Surface(self.image.get_size())
		changed_image.fill("#FFFFFF")
		changed_image.blit(self.image, (0, 0), special_flags=pygame.BLEND_SUB)
		changed_image.set_colorkey("#FFFFFF")
		self.image = changed_image

	'''改变速度方向'''
	def changeSpeed(self, direction):
		if direction[0] < 0:
			self.image = pygame.transform.flip(self.base_image, True, False)
		elif direction[0] > 0:
			self.image = self.base_image.copy()
		elif direction[1] < 0:
			self.image = pygame.transform.rotate(self.base_image, 90)
		elif direction[1] > 0:
			self.image = pygame.transform.rotate(self.base_image, -90)
		if self.weak:
			self.change_image()
		self.speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]
		return self.speed
	
	'''更新角色位置'''
	def update(self, wall_sprites, gate) -> bool:
		if gate and not self.is_move:
			return False
		x_prev = self.rect.left
		y_prev = self.rect.top
		self.rect.left += self.speed[0]
		self.rect.top += self.speed[1]
		if (
			pygame.sprite.spritecollide(self, wall_sprites, False)
	  		or gate is not None
			and pygame.sprite.collide_rect(self, gate)
		):
			self.rect.left = x_prev
			self.rect.top = y_prev
			return False
		return True
