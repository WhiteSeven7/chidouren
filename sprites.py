'''
Function:
	定义一些精灵类
'''
import pygame
import random
from data import *
import copy


'''墙类'''
class Wall(pygame.sprite.Sprite):
	def __init__(self, rect, color):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(rect)
		self.image = pygame.Surface(self.rect.size)
		self.image.fill(color)


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
		self.magic = random.choice(self.magic_list)
		if not self.magic:
			width, height = 6, 6
			color = YELLOW
		else:
			width, height = 12, 12
			if self.magic == 'strong':
				color = RED
			elif self.magic == 'view':
				color = GREEN

		pygame.sprite.Sprite.__init__(self)
		if self.magic != 'score':
			self.image = pygame.Surface((width, height)).convert_alpha()
			self.image.fill("#00000000")
			pygame.draw.ellipse(self.image, color, (0, 0, width, height))
		else:
			self.image = pygame.image.load(ORANGEPATH).convert_alpha()
		self.rect = self.image.get_rect(center=(x,y))




'''角色类'''
class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, role_image_path, tracks=None, track_restart=0, is_move=True):
		pygame.sprite.Sprite.__init__(self)
		self.role_name_path = role_image_path
		self.base_image = pygame.image.load(role_image_path).convert_alpha()
		self.image = self.base_image.copy()
		self.rect = self.image.get_rect(center=(x, y))
		self.prev_x = x
		self.prev_y = y
		self.base_speed = [30, 30]
		self.speed = [0, 0]
		self.is_move = is_move
		self.tracks = [] if tracks is None else tracks
		self.track_index = 0
		self.track_restart = track_restart


	'''特殊变色'''
	def change_image(self):
		changed_image = pygame.Surface(self.image.get_size())
		changed_image.fill("#FFFFFF")
		changed_image.blit(self.image, (0, 0), special_flags=pygame.BLEND_SUB)
		changed_image.set_colorkey("#FFFFFF")
		self.image = changed_image

	'''改变速度方向'''
	def changeSpeed(self, direction):
		self.speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]
		return self.speed
	
	'''改变图片朝向'''
	def tansformImage(self, direction):
		if direction[0] < 0:
			self.image = pygame.transform.flip(self.base_image, True, False)
		elif direction[0] > 0:
			self.image = self.base_image.copy()
		elif direction[1] < 0:
			self.image = pygame.transform.rotate(self.base_image, 90)
		elif direction[1] > 0:
			self.image = pygame.transform.rotate(self.base_image, -90)


	'''更新玩家位置'''
	def playerUpdate(self, wall_sprites, gate, god_mode: bool):
		self.tansformImage(self.speed)
		if not self.is_move:
			return False
		x_prev = self.rect.left
		y_prev = self.rect.top
		self.rect.left += self.speed[0]
		self.rect.top += self.speed[1]
		if god_mode:
			return True
		if pygame.sprite.spritecollide(self, wall_sprites, False) \
			or pygame.sprite.collide_rect(self, gate):
			self.rect.left = x_prev
			self.rect.top = y_prev
			return False
		return True


	'''更新怪物位置'''
	def ghostUpdate(self, wall_sprites, magic_times: dict[str, int]) -> bool:
		self.tansformImage(self.speed)
		if magic_times is not None and magic_times['strong']:
			self.change_image()
		x_prev = self.rect.left
		y_prev = self.rect.top
		self.rect.left += self.speed[0]
		self.rect.top += self.speed[1]
		if (pygame.sprite.spritecollide(self, wall_sprites, False)):
			self.rect.left = x_prev
			self.rect.top = y_prev
			return False
		return True
	
	'''复制的自己'''
	def copy(self) -> "Player":
		shadow = self.__class__(
			self.rect.centerx, self.rect.centery, self.role_name_path, 
			self.tracks, self.track_restart, self.is_move, 
		)
		shadow.prev_x = self.prev_x
		shadow.prev_y = self.prev_y
		shadow.base_speed = self.base_speed
		shadow.speed = self.speed
		shadow.track_index = self.track_index
		return shadow
