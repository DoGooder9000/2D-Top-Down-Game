import pygame

pygame.init()


def Update():
    pygame.display.update()


window_size = (600, 800)
window_width, window_height = window_size
title = "Top Down Shooter"

window = pygame.display.set_mode(window_size)
pygame.display.set_caption(title)

clock = pygame.time.Clock()

running = True
FPS = 60


while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    Update()