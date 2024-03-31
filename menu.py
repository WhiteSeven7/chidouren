import pygame
import sys


def main_menu(font: pygame.font.Font):
	clock = pygame.time.Clock()
	surf = pygame.display.get_surface()
	imgs = (
		font.render("开始游戏", True, "#000000", "#FFFFFF"),
		font.render("排行榜", True, "#000000", "#FFFFFF")
	)
	buttons = [
		(img, img.get_rect(center=(surf.get_width()/2,surf.get_height()*i/3)))
		for i, img in enumerate(imgs, 1)
	]
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if buttons[0][1].collidepoint(event.pos):
					print("开始游戏")
				elif buttons[1][1].collidepoint(event.pos):
					print("排行榜")
		surf.fill((128, 128, 128))
		surf.blits(buttons)
		pygame.display.flip()
		clock.tick()
	return True


def score_lock(font_small):
	...
