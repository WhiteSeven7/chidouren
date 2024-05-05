'''
Function:
	定义关卡
'''
import pygame
from sprites import *
from data import *


class Level():
	def __init__(self) -> None:
		# setupWalls 墙
		self.wall_sprites = pygame.sprite.Group()
		self.core_walls = pygame.sprite.Group()
		self._setupWalls(SKYBLUE)
		# setupGate 门
		self.gate = Wall((276, 242, 54, 2), WHITE)
		self.gate_sprites = pygame.sprite.GroupSingle(self.gate)
		# setupPlayers 玩家与怪物
		self.hero = Player(303, 453, HEROPATH)
		self.hero_sprites = pygame.sprite.GroupSingle(self.hero)
		self.ghost_sprites = pygame.sprite.Group()
		self._setupPlayers()
		# setupFood 食物
		self.food_sprites = pygame.sprite.Group()
  
	def create(self):
		self._setupFood()

	'''创建墙'''
	def _setupWalls(self, wall_color):
		core_walls = [
			(240, 240, 36, 6),
			(240, 300, 126, 6),
			(360, 240, 6, 66),
			(330, 240, 36, 6),
			(240, 240, 6, 66),
		]
		wall_rects = [
			(0, 0, 6, 606),
			(0, 0, 606, 6),
			(0, 600, 606, 6),
			(600, 0, 6, 606),
			(300, 0, 6, 66),
			(60, 60, 186, 6),
			(360, 60, 186, 6),
			(60, 120, 66, 6),
			(60, 120, 6, 126),
			(180, 120, 246, 6),
			(300, 120, 6, 66),
			(480, 120, 66, 6),
			(540, 120, 6, 126),
			(120, 180, 126, 6),
			(120, 180, 6, 126),
			(360, 180, 126, 6),
			(480, 180, 6, 126),
			(180, 240, 6, 126),
			(180, 360, 246, 6),
			(420, 240, 6, 126),
			(240, 240, 36, 6),
			(330, 240, 36, 6),
			(240, 240, 6, 66),
			(240, 300, 126, 6),
			(360, 240, 6, 66),
			(0, 300, 66, 6),
			(540, 300, 66, 6),
			(60, 360, 66, 6),
			(60, 360, 6, 186),
			(480, 360, 66, 6),
			(540, 360, 6, 186),
			(120, 420, 366, 6),
			(120, 420, 6, 66),
			(480, 420, 6, 66),
			(180, 480, 246, 6),
			(300, 480, 6, 66),
			(120, 540, 126, 6),
			(360, 540, 126, 6),
		]
		for wall_rect in wall_rects:
			wall = Wall(wall_rect, wall_color)
			self.wall_sprites.add(wall)
			if wall_rect in core_walls:
				self.core_walls.add(wall)
	
	'''创建角色'''
	def _setupPlayers(self) -> tuple[Player, pygame.sprite.GroupSingle, pygame.sprite.Group]:
		# Blinky
		self.ghost_sprites.add(Player(303, 213, BlinkyPATH, True, TRACKSMAP[BlinkyPATH]))
		# Clyde
		self.ghost_sprites.add(Player(333, 273, ClydePATH, True, TRACKSMAP[ClydePATH], 3))
		# Inky
		self.ghost_sprites.add(Player(273, 273, InkyPATH, True, TRACKSMAP[InkyPATH], 15))
		# Pinky
		self.ghost_sprites.add(Player(303, 273, PinkyPATH, True, TRACKSMAP[PinkyPATH], 9))
	
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
	def _setupFood(self):
		for row in range(1, 20):
			for col in range(1, 20):
				if row in (8, 9) and col in (8, 9, 10):
					continue
				food = Food(30*col, 30*row)
				if (pygame.sprite.spritecollide(food, self.wall_sprites, False)
		 			or pygame.sprite.collide_rect(food, self.gate)
					or pygame.sprite.collide_rect(food, self.hero)):
					continue
				self.food_sprites.add(food)
				
	def getWalls(self):
		return self.wall_sprites

	def  getGate(self):
		return self.gate, self.gate_sprites

	def  getPlayers(self):
		return self.hero, self.hero_sprites, self.ghost_sprites

	def  getFood(self):
		return self.food_sprites
