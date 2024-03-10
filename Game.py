'''
Function:
	吃豆豆小游戏
'''
import os
import sys
import pygame
import levels
import sprites


'''定义一些必要的参数'''
SIZE = 686, 606
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 191, 255)
BGMPATH = os.path.join(os.getcwd(), 'resources/sounds/bg.mp3')
ICONPATH = os.path.join(os.getcwd(), 'resources/images/icon.png')
FONTPATH = os.path.join(os.getcwd(), 'resources/font/SmileySans-Oblique.ttf')


'''用户事件'''
class UserEvent:
    order = pygame.USEREVENT

    def __new__(cls):
        cls.order += 1
        return cls.order


ADDGHOST = UserEvent()


'''开始某一关游戏'''
def startLevelGame(level: levels.Level, screen: pygame.Surface, font: pygame.font.Font):
	clock = pygame.time.Clock()
	SCORE = 0
	wall_sprites = level.setupWalls(SKYBLUE)
	gate, gate_sprites = level.setupGate(WHITE)
	hero, hero_sprites, ghost_sprites = level.setupPlayers()
	food_sprites = level.setupFood()
	move_time = 0
	move_COOL = 200
	magic_times = {
		'strong': 0,
		'view': 0
	}
	while True:
		# control
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == ADDGHOST:
				level.add_ghost(event.role_name_path)
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
			hero.update(wall_sprites, gate)
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
			ghosts_move(ghost_sprites, wall_sprites, magic_times)
		# draw
		screen.fill(BLACK)
		hero_sprites.draw(screen)
		wall_sprites.draw(screen)
		gate_sprites.draw(screen)
		food_sprites.draw(screen)
		ghost_sprites.draw(screen)
		# 得分
		score_text = font.render("得分：%s" % SCORE, True, RED)
		screen.blit(score_text, score_text.get_rect(center=(642, 30)))
		# 技能
		if strong:= magic_times['strong']:
			strong_text1 = font.render(f"幽灵弱化", True, RED)
			screen.blit(strong_text1, strong_text1.get_rect(center=(642, 472)))
			strong_text2 = font.render(f"{strong / 1000:.1f}", True, RED)
			screen.blit(strong_text2, strong_text2.get_rect(center=(642, 502)))
		if view:= magic_times['view']:
			view_text1 = font.render(f"幽灵路径", True, GREEN)
			screen.blit(view_text1, view_text1.get_rect(center=(642, 532)))
			view_text2 = font.render(f"{view / 1000:.1f}", True, GREEN)
			screen.blit(view_text2, view_text2.get_rect(center=(642, 562)))
		pygame.display.flip()
		# 成功通过
		if len(food_sprites) == 0:
			return True
		# 被杀死
		if magic_times['strong']:
			ghost: sprites.Player
			for ghost in pygame.sprite.spritecollide(hero, ghost_sprites, True):
				pygame.time.set_timer(
					pygame.event.Event(ADDGHOST, {'role_name_path': ghost.role_name_path}),
					4000, 1
				)
		elif pygame.sprite.spritecollide(hero, ghost_sprites, False):
			return False
		clock.tick(60)


'''幽灵移动'''
def ghosts_move(ghost_sprites, wall_sprites, magic_times):
	from sprites import Player
	ghost: Player
	for ghost in ghost_sprites:
		# 指定幽灵运动路径
		tracks_loc = ghost.tracks_loc
		if tracks_loc[1] < ghost.tracks[tracks_loc[0]][2]:
			ghost.changeSpeed(ghost.tracks[tracks_loc[0]][0: 2], magic_times)
			tracks_loc[1] += 1
		else:
			if tracks_loc[0] < len(ghost.tracks) - 1:
				tracks_loc[0] += 1
			elif ghost.role_name_path == levels.ClydePATH:
				tracks_loc[0] = 2
			else:
				tracks_loc[0] = 0
			ghost.changeSpeed(ghost.tracks[tracks_loc[0]][0: 2], magic_times)
			tracks_loc[1] = 0
		if tracks_loc[1] < ghost.tracks[tracks_loc[0]][2]:
			ghost.changeSpeed(ghost.tracks[tracks_loc[0]][0: 2], magic_times)
		else:
			if tracks_loc[0] < len(ghost.tracks) - 1:
				loc0 = tracks_loc[0] + 1
			elif ghost.role_name_path == levels.ClydePATH:
				loc0 = 2
			else:
				loc0 = 0
			ghost.changeSpeed(ghost.tracks[loc0][0: 2], magic_times)
		ghost.update(wall_sprites, None)


'''显示文字'''
def showText(screen: pygame.Surface, font: pygame.font.Font, is_clearance: bool):
	clock = pygame.time.Clock()
	msg = '游戏结束了！' if not is_clearance else '恭喜，你胜利了！'
	bg = pygame.Surface((400, 200))
	bg.fill((128, 128, 128))
	texts = [
		font.render(msg, True, WHITE),
		font.render('按“回车”重新游玩', True, WHITE),
		font.render('按“ESC”退出游戏', True, WHITE)
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
				elif event.key == pygame.K_ESCAPE:
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
	while True:
		level = levels.Level()
		is_clearance = startLevelGame(level, screen, font_small)
		if showText(screen, font_big, is_clearance):
			break
	pygame.quit()
	sys.exit()
	

'''test'''
if __name__ == '__main__':
	screen = initialize()
	main(screen)
