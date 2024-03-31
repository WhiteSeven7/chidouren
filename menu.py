import pygame
import sys
import json


def main_menu(font: pygame.font.Font):
	clock = pygame.time.Clock()
	bg = pygame.image.load("resources/images/bg.png")
	surf = pygame.display.get_surface()
	imgs = (
		font.render("开始游戏", True, "#000000", "#FFFFFF"),
		font.render("排行榜", True, "#000000", "#FFFFFF"),
		font.render("退出游戏", True, "#000000", "#FFFFFF"),
	)
	buttons = [
		(img, img.get_rect(center=(surf.get_width()/2,surf.get_height()*i/4)))
		for i, img in enumerate(imgs, 1)
	]
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if buttons[0][1].collidepoint(event.pos):
					return True
				elif buttons[1][1].collidepoint(event.pos):
					return False
				elif buttons[2][1].collidepoint(event.pos):
					pygame.quit()
					sys.exit()
		surf.blit(bg, (0, 0))
		surf.blits(buttons)
		pygame.display.flip()
		clock.tick(60)


'''拿到成绩数据'''
def get_score_data():
	with open("score_lock.json", 'r', encoding='utf-8') as file:
		score_data = json.load(file)
	return [tuple(score) for score in score_data]


'''保存数据'''
def save_score_data(score_data):
	with open("score_lock.json", 'w', encoding='utf-8') as file:
		json.dump(score_data, file)


def score_lock(font:pygame.font.Font, score_data: list[tuple[str, bool, int]]):
	delete = False
	clock = pygame.time.Clock()
	surf = pygame.display.get_surface()
	center_x = surf.get_width()/4
	score_img_rect = []
	bottom = 20
	for i, (datatime, is_win, score) in enumerate(score_data[:20]):
		img = font.render(f'{datatime} {"胜利" if is_win else "失败":>6} {score:>6}', True, '#FFFFFF', '#000000')
		rect = img.get_rect(midtop=(center_x, bottom+20))
		bottom = rect.bottom
		score_img_rect.append((img, rect))
		if i == 9:
			center_x *= 3
			bottom = 20
	button_img = font.render("返回", True, '#000000', '#FFFFFF')
	button_rect = button_img.get_rect(midbottom=(surf.get_width()/3, surf.get_height()-40))
	clear_img = font.render("清除数据", True, '#FF0000', '#FFFFFF')
	clear_rect = clear_img.get_rect(midbottom=(surf.get_width()*2/3, surf.get_height()-40))
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if button_rect.collidepoint(event.pos):
					return
				elif clear_rect.collidepoint(event.pos):
					score_data.clear()
					score_img_rect.clear()
					save_score_data(score_data)
		surf.fill((60, 60, 60))
		surf.blits(score_img_rect)
		surf.blit(button_img, button_rect)
		surf.blit(clear_img, clear_rect)
		pygame.display.flip()
		clock.tick(60)
		