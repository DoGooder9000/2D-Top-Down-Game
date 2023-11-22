import pygame
from math import sin, cos, tan, radians

pygame.init()

def DrawMap(color: tuple):
	for r in range(len(map)):
		for t in range(len(map[r])):
			if map[r][t] == "X":
				pygame.draw.rect(window, color, pygame.Rect((t*tile_width, r*tile_height), (tile_width, tile_height)))

def DrawPlayer(color: tuple, radius: float = 2):
	pygame.draw.circle(window, color, PlayerPos, radius)

def Update():
	pygame.display.update()


window_size = (600, 800)
window_width, window_height = window_size
title = "Top Down Shooter"

window = pygame.display.set_mode(window_size)
pygame.display.set_caption(title)


PlayerPos = (window_width/2, window_height/2)
PlayerAngle = 0

PlayerSpeed = 1.5
PlayerTurningSpeed = 1


map = [
	"XXXXXXXXXXXXX",
	"X           X",
	"X  XX XXX   X",
	"X  X   X    X",
	"X  X    XXX X",
	"X  XXXX   X X",
	"X      X  X X",
	"XXXXXXXXXXX X",
	"X           X",
	"X  XXXX     X",
	"X  X  X     X",
	"X  XXXX     X",
	"X           X",
	"XXXXXXXXXXXXX",
	]

tile_width = window_width/len(map[0])
tile_height = window_height/len(map)

white = (255, 255, 255)
black = (0, 0, 0)
red = 	(255, 0, 0)
green = (0, 255, 0)
blue = 	(0, 0, 255)

clock = pygame.time.Clock()

running = True
FPS = 60


while running:
	dt = clock.tick(FPS)/10

	pygame.display.set_caption(f"Wolfenstien 3D Renderer FPS: {int(clock.get_fps())}")

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	keys = pygame.key.get_pressed()

	if keys[pygame.K_w]:
		PlayerPos = (PlayerPos[0]+cos(PlayerAngle)*PlayerSpeed*dt, PlayerPos[1]+sin(PlayerAngle)*PlayerSpeed*dt)
	if keys[pygame.K_s]:
		PlayerPos = (PlayerPos[0]-cos(PlayerAngle)*PlayerSpeed*dt, PlayerPos[1]-sin(PlayerAngle)*PlayerSpeed*dt)
	if keys[pygame.K_a]:
		PlayerAngle -= radians(PlayerTurningSpeed*dt)
	if keys[pygame.K_d]:
		PlayerAngle += radians(PlayerTurningSpeed*dt)
	
	window.fill((100, 100, 100))

	DrawMap(white)

	DrawPlayer(blue)
	
	Update()