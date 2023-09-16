import pygame
from rng import rng
from map import Map

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
chunk_size = 9
roughness = 0.1
gradient = 90
load_distance = 1
tile_size = 16
min_value = 0
max_value = 255
offset = 0
map = Map(chunk_size, roughness, gradient, load_distance,  tile_size, offset, min_value, max_value)
map.draw_visible_map(screen, 0,0)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)  # limits FPS to 60

pygame.quit()