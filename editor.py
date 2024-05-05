import pygame
import sys

import pygame.locals
from levels import Level
import levels
from sprites import *


def to_g(pos):
	return (pos[0] + 15 - 3) // 30, (pos[1] + 15 - 3) // 30


def to_r(pos):
	return pos[0] * 30 + 3, pos[1] * 30 + 3


def in_(pos):
	x, y = pos
	x = 0 if x < 0 else 20 if x > 20 else x
	y = 0 if y < 0 else 20 if y > 20 else y
	return x, y


class Button(pygame.sprite.Sprite):
	def __init__(self, img_path, center) -> None:
		super().__init__()
		self.img_path = img_path
		self.image = pygame.surface.Surface((50, 50))
		self.rect = self.image.get_rect(center=center)
		if img_path:
			img = pygame.image.load(img_path).convert_alpha()
			x = (self.image.get_width() - img.get_width()) / 2
			y = (self.image.get_height() - img.get_height()) / 2
			self.image.blit(img, (x, y))
		else:
			pygame.draw.rect(self.image, SKYBLUE, (10, 10, 30, 30), 3)


'''关卡编辑器'''
def editor(level: Level):
	screen = pygame.display.get_surface()
	clock = pygame.time.Clock()
	mode = ''
	buttons = pygame.sprite.Group(
		Button('', (653, 60 * 1)),
		Button(HEROPATH, (653, 60 * 2)),
		Button(BlinkyPATH, (653, 60 * 3)),
		Button(ClydePATH, (653, 60 * 4)),
		Button(InkyPATH, (653, 60 * 5)),
		Button(PinkyPATH, (653, 60 * 6)),
	)
	picked = None
	write_start_g = None
	write_rect = None
	while True:
		if pygame.event.get(pygame.QUIT):
			pygame.quit()
			sys.exit()
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				return
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				for button in buttons:
					if button.rect.collidepoint(event.pos):
						mode = button.img_path
						if mode == '':
							picked = None
						if mode == level.hero.role_name_path:
							picked = level.hero
						else:
							for ghost in level.ghost_sprites:
								if mode == ghost.role_name_path:
									picked = ghost
									break
						break
			if mode == '':
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					x, y = to_g(event.pos)
					if 0 <= x <= 20 and 0 <= y <= 20:
						write_start_g = x, y
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and write_start_g is not None:
					level.wall_sprites.add(Wall(write_rect, levels.SKYBLUE))
					write_start_g = None
					write_rect = None
			else:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						...
					elif event.button == 3:
						...
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						picked.rect.move_ip(-30, 0)
					elif event.key == pygame.K_RIGHT:
						picked.rect.move_ip(30, 0)
					elif event.key == pygame.K_UP:
						picked.rect.move_ip(0, -30)
					elif event.key == pygame.K_DOWN:
						picked.rect.move_ip(0, 30)
		mouse_pos = pygame.mouse.get_pos()
		if mode == '':
			left, _, right = pygame.mouse.get_pressed()
			if right and not left:
				for wall in level.wall_sprites:
					if wall.rect.collidepoint(mouse_pos) and wall not in level.core_walls:
						wall.kill()
		else:
			...
		screen.fill('#000000')
		# 游戏元素
		level.wall_sprites.draw(screen)
		level.gate_sprites.draw(screen)
		level.ghost_sprites.draw(screen)
		level.hero_sprites.draw(screen)
		# 画墙
		if write_start_g:
			mouse_pos_g = in_(to_g(mouse_pos))
			width, height = abs(write_start_g[0] - mouse_pos_g[0]), abs(write_start_g[1] - mouse_pos_g[1])
			if width < height:
				# 竖线
				write_rect = pygame.Rect(
					write_start_g[0] * 30, min(write_start_g[1], mouse_pos_g[1]) * 30, 6, height * 30 + 6)
			else:
				# 横线
				write_rect = pygame.Rect(
					min(write_start_g[0], mouse_pos_g[0]) * 30, write_start_g[1] * 30, width * 30 + 6, 6)
			pygame.draw.rect(screen, '#ffffff', write_rect)
		# 格子线
		for i in range(21):
			pygame.draw.line(screen, '#dddddd', (i * 30 + 15 + 3, 3), (i * 30 + 15 + 3, screen.get_height()))
		for i in range(20):
			pygame.draw.line(screen, '#dddddd', (3, i * 30 + 15 + 3), (20 * 30 + 15 + 3, i * 30 + 15 + 3))
		# 选项
		buttons.draw(screen)
		for button in buttons:
			if button.img_path == mode:
				pygame.draw.rect(screen, '#FFFFFF', button.rect, 5)
		pygame.display.flip()
		clock.tick(60)
