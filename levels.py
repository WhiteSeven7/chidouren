'''
Function:
	定义关卡
'''
import pygame
from sprites import *


NUMLEVELS = 1


class Level():

	'''创建墙'''
	def setupWalls(self, wall_color):
		self.wall_sprites = pygame.sprite.Group()
		wall_positions = [[0, 0, 6, 600],
						  [0, 0, 600, 6],
						  [0, 600, 606, 6],
						  [600, 0, 6, 606],
						  [300, 0, 6, 66],
						  [60, 60, 186, 6],
						  [360, 60, 186, 6],
						  [60, 120, 66, 6],
						  [60, 120, 6, 126],
						  [180, 120, 246, 6],
						  [300, 120, 6, 66],
						  [480, 120, 66, 6],
						  [540, 120, 6, 126],
						  [120, 180, 126, 6],
						  [120, 180, 6, 126],
						  [360, 180, 126, 6],
						  [480, 180, 6, 126],
						  [180, 240, 6, 126],
						  [180, 360, 246, 6],
						  [420, 240, 6, 126],
						  [240, 240, 42, 6],
						  [324, 240, 42, 6],
						  [240, 240, 6, 66],
						  [240, 300, 126, 6],
						  [360, 240, 6, 66],
						  [0, 300, 66, 6],
						  [540, 300, 66, 6],
						  [60, 360, 66, 6],
						  [60, 360, 6, 186],
						  [480, 360, 66, 6],
						  [540, 360, 6, 186],
						  [120, 420, 366, 6],
						  [120, 420, 6, 66],
						  [480, 420, 6, 66],
						  [180, 480, 246, 6],
						  [300, 480, 6, 66],
						  [120, 540, 126, 6],
						  [360, 540, 126, 6]]
		for wall_position in wall_positions:
			wall = Wall(*wall_position, wall_color)
			self.wall_sprites.add(wall)
		return self.wall_sprites
	
	'''创建门'''
	def setupGate(self, gate_color):
		self.gate = Wall(282, 242, 42, 2, gate_color)
		return self.gate, pygame.sprite.GroupSingle(self.gate)
	
	'''创建角色'''
	def setupPlayers(self, hero_image_path, ghost_images_path) -> tuple[Player, pygame.sprite.GroupSingle, pygame.sprite.Group]:
		self.hero = Player(287, 439, hero_image_path)
		ghost_sprites = pygame.sprite.Group()
		for each in ghost_images_path:
			role_name = each.split('/')[-1].split('.')[0]
			if role_name == 'Blinky':
				tracks = [
					[0, -0.5, 4], [0.5, 0, 9], [0, 0.5, 11], [0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 11], [0, 0.5, 3],
					[0.5, 0, 15], [0, -0.5, 15], [0.5, 0, 3], [0, -0.5, 11], [-0.5, 0, 3], [0, -0.5, 11], [-0.5, 0, 3],
					[0, -0.5, 3], [-0.5, 0, 7], [0, -0.5, 3], [0.5, 0, 15], [0, 0.5, 15], [-0.5, 0, 3], [0, 0.5, 3],
					[-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7], [0.5, 0, 5]
				]
				ghost_sprites.add(Player(287, 199, each, True, tracks))
			elif role_name == 'Clyde':
				tracks = [
					[-1, 0, 2], [0, -0.5, 4], [0.5, 0, 5], [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7],
					[-0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 7], [0, 0.5, 15], [0.5, 0, 15], [0, -0.5, 3],
					[-0.5, 0, 11], [0, -0.5, 7], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 9]
				]
				ghost_sprites.add(Player(319, 259, each, True, tracks))
			elif role_name == 'Inky':
				tracks = [
					[1, 0, 2], [0, -0.5, 4], [0.5, 0, 10], [0, 0.5, 7], [0.5, 0, 3], [0, -0.5, 3],
					[0.5, 0, 3], [0, -0.5, 15], [-0.5, 0, 15], [0, 0.5, 3], [0.5, 0, 15], [0, 0.5, 11],
					[-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 11], [0, 0.5, 3], [-0.5, 0, 11], [0, 0.5, 7],
					[-0.5, 0, 3], [0, -0.5, 3], [-0.5, 0, 3], [0, -0.5, 15], [0.5, 0, 15], [0, 0.5, 3],
					[-0.5, 0, 15], [0, 0.5, 11], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 11], [0, 0.5, 3], [0.5, 0, 1]
				]
				ghost_sprites.add(Player(255, 259, each, True, tracks))
			elif role_name == 'Pinky':
				tracks = [
					[0, -1, 4], [0.5, 0, 9], [0, 0.5, 11], [-0.5, 0, 23], [0, 0.5, 7], [0.5, 0, 3],
					[0, -0.5, 3], [0.5, 0, 19], [0, 0.5, 3], [0.5, 0, 3], [0, 0.5, 3], [0.5, 0, 3],
					[0, -0.5, 15], [-0.5, 0, 7], [0, 0.5, 3], [-0.5, 0, 19], [0, -0.5, 11], [0.5, 0, 9]
				]
				ghost_sprites.add(Player(287, 259, each, True, tracks))
		return self.hero, pygame.sprite.GroupSingle(self.hero), ghost_sprites
	
	'''创建食物'''
	def setupFood(self):
		self.food_sprites = pygame.sprite.Group()
		for row in range(19):
			for col in range(19):
				if row in (8, 9) and col in (8, 9, 10):
					continue
				food = Food(30*col+31, 30*row+3)
				if (pygame.sprite.spritecollide(food, self.wall_sprites, False)
		 			or pygame.sprite.collide_rect(food, self.gate)):
					continue
				self.food_sprites.add(food)
		return self.food_sprites
