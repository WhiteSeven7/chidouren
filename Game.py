'''
Function:
	吃豆豆小游戏
'''
import os
import sys
import pygame
import levels
import sprites
from menu import *
import datetime
from levels import WHITE
from editor import *
from data import *




'''开始某一关游戏'''
def startLevelGame(
		level: levels.Level, screen: pygame.Surface, font: pygame.font.Font, level_index: int
	) -> tuple[bool, int]:
	level.create()
	clock = pygame.time.Clock()
	SCORE = 0
	wall_sprites = level.getWalls()
	gate, gate_sprites = level.getGate()
	hero, hero_sprites, ghost_sprites = level.getPlayers()
	food_sprites = level.getFood()
	move_time = 0
	move_COOL = 200
	magic_times = {
		'strong': 0,
		'view': 0
	}
	# 上帝模式
	god_mode = False
	ghost_index = 0
	# 文字
	fade = font.render(f"幽灵弱化", True, RED)
	path = font.render(f"幽灵路径", True, GREEN)
	index = font.render(f"第{level_index}关", True, WHITE)
	god_img = font.render(f"上帝模式", True, WHITE)
	ghost_move = False
	while True:
		# control
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif 0 <= event.type - pygame.USEREVENT < 4:
				level.add_ghost(event.role_name_path)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_x:
					god_mode = not god_mode
				elif event.key == pygame.K_p:
					pygame.quit()
					sys.exit()
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			hero.changeSpeed([-1, 0])
			hero.is_move = True
		elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			hero.changeSpeed([1, 0])
			hero.is_move = True
		elif keys[pygame.K_UP] or keys[pygame.K_w]:
			hero.changeSpeed([0, -1])
			hero.is_move = True
		elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
			hero.changeSpeed([0, 1])
			hero.is_move = True
		else:
			hero.is_move = False
		# 魔法效果流失
		for magic in magic_times:
			magic_times[magic] = max(magic_times[magic] - clock.get_time(), 0)
		# update
		move_time += clock.get_time()
		if move_time >= move_COOL:
			move_time -= move_COOL
			# 玩家移动位子
			hero.playerUpdate(wall_sprites, gate, god_mode)
			# 玩家吃果子
			food_eaten = pygame.sprite.spritecollide(hero, food_sprites, True)
			SCORE += len(food_eaten)
			# 获得魔法
			food: sprites.Food
			for food in food_eaten:
				if food.magic in magic_times:
					magic_times[food.magic] += 8000
				elif food.magic == 'score':
					# 额外i得分
					SCORE += 4
			# 幽灵移动
			if ghost_move:
				ghosts_move(ghost_sprites, wall_sprites, magic_times)
			ghost_move = not ghost_move
		# draw
		screen.fill(BLACK)
		wall_sprites.draw(screen)
		gate_sprites.draw(screen)
		food_sprites.draw(screen)
		ghost_sprites.draw(screen)
		# 预知
		if magic_times['view']:
			for i in range(5):
				shadow_ghost_sprites = pygame.sprite.Group()
				for ghost in ghost_sprites:
					shadow_ghost_sprites.add(ghost.copy())
				for _ in range(i + 1):
					ghosts_move(shadow_ghost_sprites, wall_sprites, magic_times)
				for ghost in shadow_ghost_sprites:
					ghost.image.set_alpha(200*(5-i)/6)
				shadow_ghost_sprites.draw(screen)
		hero_sprites.draw(screen)
		# 关卡
		level_draw_text(index, (642, 30), hero)
		# 得分
		level_draw_text(font.render("得分：%s" % SCORE, True, RED), (642, 60), hero)
		# 魔法
		if strong := magic_times['strong']:
			level_draw_text(fade, (642, 472), hero)
			level_draw_text(font.render(f"{strong / 1000:.1f}", True, RED), (642, 502), hero)
		if view:= magic_times['view']:
			level_draw_text(path, (642, 532), hero)
			level_draw_text(font.render(f"{view / 1000:.1f}", True, GREEN), (642, 562), hero)
		# 上帝
		if god_mode:
			level_draw_text(god_img, (642, SIZE[1]/2), hero)
		pygame.display.flip()
		# 成功通过
		if len(food_sprites) == 0:
			return True, SCORE
		# 被杀死
		if magic_times['strong']:
			ghost: sprites.Player
			for ghost in pygame.sprite.spritecollide(hero, ghost_sprites, True):
				pygame.time.set_timer(
					pygame.event.Event(pygame.USEREVENT + ghost_index, {'role_name_path': ghost.role_name_path}),
					4000, 1
				)
				ghost_index = (ghost_index + 1) % 4
		elif not god_mode and pygame.sprite.spritecollide(hero, ghost_sprites, False):
			return False, SCORE
		clock.tick(60)


'''幽灵移动'''
def ghosts_move(ghost_sprites, wall_sprites, magic_times):
	from sprites import Player
	ghost: Player
	for ghost in ghost_sprites:
		tracks = ghost.tracks
		if ghost.rect.collidepoint(tracks[ghost.track_index][0]):
			ghost.changeSpeed(tracks[ghost.track_index][1])
			ghost.track_index += 1
			if ghost.track_index >= len(tracks):
				ghost.track_index = ghost.track_restart
		ghost.ghostUpdate(wall_sprites, magic_times)


'''绘制文字'''
def level_draw_text(
		text_img: pygame.Surface, center: tuple[int, int],
		hero: levels.Player
	) -> None:
	rect = text_img.get_rect(center=center)
	# 彩蛋
	if not rect.colliderect(hero.rect):
		screen.blit(text_img, rect)


'''显示文字'''
def showText(screen: pygame.Surface, font: pygame.font.Font, is_clearance: bool):
	clock = pygame.time.Clock()
	msg = '游戏结束了！' if not is_clearance else '恭喜，你胜利了！'
	bg = pygame.Surface((400, 200))
	bg.fill((128, 128, 128))
	texts = [
		font.render(msg, True, WHITE),
		font.render('按“回车”重新游玩', True, WHITE),
		font.render('按“ESC”或“p”回到菜单', True, WHITE)
	]
	positions = [
		img.get_rect(center=(SIZE[0]/2,SIZE[1]/2+(i-1)*2*img.get_height()))
		for i, img in enumerate(texts)
	]
	while True:
		# 控制
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return False
				elif event.key in (pygame.K_ESCAPE, pygame.K_p):
					return True
		# 绘制
		screen.fill(BLACK)
		screen.blit(bg, bg.get_rect(center=(SIZE[0]/2,SIZE[1]/2)))
		for text, position in zip(texts, positions):
			screen.blit(text, position)
		pygame.display.flip()
		clock.tick(60)


'''初始化'''
def initialize():
	pygame.init()
	icon_image = pygame.image.load(ICONPATH)
	pygame.display.set_icon(icon_image)
	screen = pygame.display.set_mode(SIZE)
	pygame.display.set_caption('吃豆人')
	return screen


'''主函数'''
def main(screen):
	pygame.mixer.init()
	pygame.mixer.music.load(BGMPATH)
	pygame.mixer.music.play(-1, 0.0)
	pygame.font.init()
	font_small = pygame.font.Font(FONTPATH, 18)
	font_big = pygame.font.Font(FONTPATH, 24)
	menu_font = pygame.font.Font(FONTPATH, 48)
	level_index = 0
	score_data = get_score_data()
	enter_menu = True
	while True:
		level = levels.Level()
		while enter_menu:
			enter_menu = True
			choice = main_menu(menu_font)
			if choice == 'game':
				break
			elif choice == 'edit':
				editor(level)
			elif choice == 'score':
				score_lock(font_big, score_data)
		level_index += 1
		is_clearance, score = startLevelGame(level, screen, font_small, level_index)
		# 记录新成绩
		score_data.append(
			(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), is_clearance, score)
		)
		score_data.sort(key=lambda x: x[2], reverse=True)
		save_score_data(score_data)
		enter_menu = showText(screen, font_big, is_clearance)
	

'''test'''
if __name__ == '__main__':
	screen = initialize()
	main(screen)
