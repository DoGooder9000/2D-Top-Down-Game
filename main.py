import pygame
import threading
from math import sin, cos, tan, atan2, radians, degrees, sqrt

pygame.init()

class Bullet:
	def __init__(self, angle: float, start_pos: tuple):
		self.angle = angle

		self.pos = BulletOffsetVector.rotate(degrees(self.angle)) + start_pos #So that the bullets looks like it is coming out of the gun
		
	
	def Update(self, color: tuple = (255, 255, 0)):
		self.pos = GetPoint(self.pos, self.angle, BulletSpeed)

		pygame.draw.circle(window, color, self.pos, BulletRadius)

		return GetTile(self.pos)

class Enemy:
	def __init__(self, pos: tuple, speed: float, size: tuple, sprite: pygame.Surface) -> None:
		self.pos = pos
		self.speed = speed
		self.size = size
		self.angle = 0
		self.originalSprite = sprite
		self.sprite = sprite
		self.rect = self.sprite.get_rect()
		self.rect.center = pos
	
	def LookAt(self, pos: tuple):
		self.angle = atan2(pos[1]-self.pos[1], pos[0]-self.pos[0])
		self.sprite = pygame.transform.rotate(self.originalSprite, -degrees(self.angle))
		self.GetRect()

	def GetRect(self):
		self.rect = self.sprite.get_rect()
		self.rect.center = self.pos
	
	def Draw(self):
		window.blit(self.sprite, self.rect)
	
	def Move(self):
		self.pos = GetPoint(self.pos, self.angle, self.speed)

class Soldier(Enemy):
	def __init__(self, pos: tuple) -> None:
		super().__init__(pos, DefaultEnemySpeed, DefaultEnemySize, SoldierSprite)


def DrawMap(color: tuple):
	for r in range(len(map)):
		for t in range(len(map[r])):
			if map[r][t] == "X":
				pygame.draw.rect(window, color, pygame.Rect((t*tile_width, r*tile_height), (tile_width, tile_height)))

def DrawPlayer():
	r = GunGuySprite.get_rect()
	r.center = PlayerPos

	window.blit(pygame.transform.rotate(GunGuySprite, -degrees(PlayerAngle)), r)

def GetTile(point: tuple):
	try:
		return map[int(point[1]/tile_height)][int(point[0]/tile_width)]
	except IndexError:
		return None

def Shoot():
	global Bullets

	Bullets.append(Bullet(PlayerAngle, PlayerPos))

def UpdateBullets():
	global Bullets, Enemies

	for bullet in Bullets:
		if bullet.Update() == "X":
			Bullets.remove(bullet)
		
		else:
			for enemy in Enemies:
				if enemy.rect.collidepoint(bullet.pos):
					Bullets.remove(bullet)
					Enemies.remove(enemy)

def HandleEnemies():
	global Enemies

	for enemy in Enemies:
		enemy.LookAt(PlayerPos)
		enemy.Move()
		enemy.Draw()

def GetPoint(start_point: tuple, angle: float, length: float):
	return (start_point[0] + cos(angle)*length, start_point[1] + sin(angle)*length)

def Distance(p1, p2):
	return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def Update():
	pygame.display.update()


window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

window_size = (600, 800)
window_width, window_height = window.get_size()
title = "Top Down Shooter"

pygame.display.set_caption(title)


PlayerPos = (window_width/2, window_height/2)
PlayerAngle = 0

PlayerSpeed = 1.5
PlayerTurningSpeed = 2

BulletSpeed = 20
BulletRadius = 2.5

BulletOffset = (12, 19)
BulletOffsetVector = pygame.math.Vector2(BulletOffset[0], BulletOffset[1])

Bullets = []


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

GunGuySize = (75, 75)
GunGuySprite = pygame.transform.scale(pygame.image.load("Sprites/TopDownGunGuy.png"), GunGuySize)

DefaultEnemySize = (75, 75)
DefaultEnemySpeed = 2.0

SoldierSprite = pygame.transform.scale(pygame.image.load("Sprites/SoldierSprite.png"), DefaultEnemySize)

Enemies = [Soldier((500, 500))]

clock = pygame.time.Clock()

running = True
FPS = 60


while running:
	dt = clock.tick(FPS)/10

	pygame.display.set_caption(f"Wolfenstien 3D Renderer FPS: {int(clock.get_fps())}")

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			Shoot()


	mousePos = pygame.mouse.get_pos()
	PlayerAngle = atan2(mousePos[1]-PlayerPos[1], mousePos[0]-PlayerPos[0])
	
	keys = pygame.key.get_pressed()

	if keys[pygame.K_w]:
		NextPos = (PlayerPos[0]+cos(PlayerAngle)*PlayerSpeed*dt, PlayerPos[1]+sin(PlayerAngle)*PlayerSpeed*dt)
		if GetTile(NextPos) != "X" and Distance(PlayerPos, mousePos) > 2: PlayerPos = NextPos
	if keys[pygame.K_s]:
		NextPos = (PlayerPos[0]-cos(PlayerAngle)*PlayerSpeed*dt, PlayerPos[1]-sin(PlayerAngle)*PlayerSpeed*dt)
		if GetTile(NextPos) != "X" and Distance(PlayerPos, mousePos) > 2: PlayerPos = NextPos
	
	window.fill((100, 100, 100))

	DrawMap(white)

	DrawPlayer()

	HandleEnemies()

	UpdateBullets()

	Update()