'''
Function:
	定义关卡
'''
import pygame
from sprites import *
import os


NUMLEVELS = 1


HEROPATH = os.path.join(os.getcwd(), 'resources/images/pacman.png')
BlinkyPATH = os.path.join(os.getcwd(), 'resources/images/Blinky.png')
ClydePATH = os.path.join(os.getcwd(), 'resources/images/Clyde.png')
InkyPATH = os.path.join(os.getcwd(), 'resources/images/Inky.png')
PinkyPATH = os.path.join(os.getcwd(), 'resources/images/Pinky.png')


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
	def setupPlayers(self) -> tuple[Player, pygame.sprite.GroupSingle, pygame.sprite.Group]:
		self.hero = Player(287, 439, HEROPATH)
		self.ghost_sprites = pygame.sprite.Group()
		tracks = [
			[0, -0.5, 4], [0.5, 0, 9], [0, 0.5, 11], [0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 11], [0, 0.5, 3],
			[0.5, 0, 15], [0, -0.5, 15], [0.5, 0, 3], [0, -0.5, 11], [-0.5, 0, 3], [0, -0.5, 11], [-0.5, 0, 3],
			[0, -0.5, 3], [-0.5, 0, 7], [0, -0.5, 3], [0.5, 0, 15], [0, 0.5, 15], [-0.5, 0, 3], [0, 0.5, 3],
			[-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7], [0.5, 0, 5]
		]
		self.ghost_sprites.add(Player(287, 199, BlinkyPATH, True, tracks))
		# Clyde
		tracks = [
			[-1, 0, 2], [0, -0.5, 4], [0.5, 0, 5], [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7],
			[-0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 7], [0, 0.5, 15], [0.5, 0, 15], [0, -0.5, 3],
			[-0.5, 0, 11], [0, -0.5, 7], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 9]
		]
		self.ghost_sprites.add(Player(319, 259, ClydePATH, True, tracks))
		# Inky
		tracks = [
			[1, 0, 2], [0, -0.5, 4], [0.5, 0, 10], [0, 0.5, 7], [0.5, 0, 3], [0, -0.5, 3],
			[0.5, 0, 3], [0, -0.5, 15], [-0.5, 0, 15], [0, 0.5, 3], [0.5, 0, 15], [0, 0.5, 11],
			[-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 11], [0, 0.5, 3], [-0.5, 0, 11], [0, 0.5, 7],
			[-0.5, 0, 3], [0, -0.5, 3], [-0.5, 0, 3], [0, -0.5, 15], [0.5, 0, 15], [0, 0.5, 3],
			[-0.5, 0, 15], [0, 0.5, 11], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 11], [0, 0.5, 3], [0.5, 0, 1]
		]
		self.ghost_sprites.add(Player(255, 259, InkyPATH, True, tracks))
		# Pinky
		tracks = [
			[0, -1, 4], [0.5, 0, 9], [0, 0.5, 11], [-0.5, 0, 23], [0, 0.5, 7], [0.5, 0, 3],
			[0, -0.5, 3], [0.5, 0, 19], [0, 0.5, 3], [0.5, 0, 3], [0, 0.5, 3], [0.5, 0, 3],
			[0, -0.5, 15], [-0.5, 0, 7], [0, 0.5, 3], [-0.5, 0, 19], [0, -0.5, 11], [0.5, 0, 9]
		]
		self.ghost_sprites.add(Player(287, 259, PinkyPATH, True, tracks))
		return self.hero, pygame.sprite.GroupSingle(self.hero), self.ghost_sprites
	
	def add_ghost(self, ghost_path):
		if ghost_path == BlinkyPATH:
			tracks = [
				[0, -0.5, 4], [0.5, 0, 9], [0, 0.5, 11], [0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 11], [0, 0.5, 3],
				[0.5, 0, 15], [0, -0.5, 15], [0.5, 0, 3], [0, -0.5, 11], [-0.5, 0, 3], [0, -0.5, 11], [-0.5, 0, 3],
				[0, -0.5, 3], [-0.5, 0, 7], [0, -0.5, 3], [0.5, 0, 15], [0, 0.5, 15], [-0.5, 0, 3], [0, 0.5, 3],
				[-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7], [0.5, 0, 5]
			]
			self.ghost_sprites.add(Player(287, 199, ghost_path, True, tracks))
		elif ghost_path == ClydePATH:
			tracks = [
				[-1, 0, 2], [0, -0.5, 4], [0.5, 0, 5], [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7],
				[-0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 7], [0, 0.5, 15], [0.5, 0, 15], [0, -0.5, 3],
				[-0.5, 0, 11], [0, -0.5, 7], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 9]
			]
			self.ghost_sprites.add(Player(319, 259, ghost_path, True, tracks))
		elif ghost_path == InkyPATH:
			tracks = [
				[1, 0, 2], [0, -0.5, 4], [0.5, 0, 10], [0, 0.5, 7], [0.5, 0, 3], [0, -0.5, 3],
				[0.5, 0, 3], [0, -0.5, 15], [-0.5, 0, 15], [0, 0.5, 3], [0.5, 0, 15], [0, 0.5, 11],
				[-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 11], [0, 0.5, 3], [-0.5, 0, 11], [0, 0.5, 7],
				[-0.5, 0, 3], [0, -0.5, 3], [-0.5, 0, 3], [0, -0.5, 15], [0.5, 0, 15], [0, 0.5, 3],
				[-0.5, 0, 15], [0, 0.5, 11], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 11], [0, 0.5, 3], [0.5, 0, 1]
			]
			self.ghost_sprites.add(Player(255, 259, ghost_path, True, tracks))
		elif ghost_path == PinkyPATH:
			tracks = [
				[0, -1, 4], [0.5, 0, 9], [0, 0.5, 11], [-0.5, 0, 23], [0, 0.5, 7], [0.5, 0, 3],
				[0, -0.5, 3], [0.5, 0, 19], [0, 0.5, 3], [0.5, 0, 3], [0, 0.5, 3], [0.5, 0, 3],
				[0, -0.5, 15], [-0.5, 0, 7], [0, 0.5, 3], [-0.5, 0, 19], [0, -0.5, 11], [0.5, 0, 9]
			]
			self.ghost_sprites.add(Player(287, 259, ghost_path, True, tracks))

	'''创建食物'''
	def setupFood(self):
		self.food_sprites = pygame.sprite.Group()
		for row in range(20):
			for col in range(19):
				if row in (8, 9) and col in (8, 9, 10):
					continue
				food = Food(30*col+31, 30*row+3)
				if (pygame.sprite.spritecollide(food, self.wall_sprites, False)
		 			or pygame.sprite.collide_rect(food, self.gate)
					or pygame.sprite.collide_rect(food, self.hero)):
					continue
				self.food_sprites.add(food)
		return self.food_sprites
