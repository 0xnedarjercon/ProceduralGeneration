import pygame
from rng import rng
from map import Map

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
chunk_size = 17
roughness = 0.75
gradient = 50
load_distance = 1200
tile_size = 16
min_value = 0
max_value = 255
offset = 0
camera_speed = 50
camera_position = [0,0]


camera_last = camera_position.copy()
map = Map(chunk_size, roughness, gradient, load_distance,  tile_size, offset, min_value, max_value)
map.draw_visible_map(screen, 0,0)
pygame.display.flip()
map.draw_visible_map(screen, 50,50)
pygame.display.flip()
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT:
        #         camera_position[1]-=camera_speed
        #     if event.key == pygame.K_RIGHT:
        #         camera_position[1]+=camera_speed
        #     if event.key == pygame.K_UP:
        #         camera_position[0]-=camera_speed
        #     if event.key == pygame.K_DOWN:
        #         camera_position[0]+=camera_speed
    
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_position[1]-=camera_speed
    if keys[pygame.K_RIGHT]:
        camera_position[1]+=camera_speed
    if keys[pygame.K_UP]:
        camera_position[0]-=camera_speed
    if keys[pygame.K_DOWN]:
        camera_position[0]+=camera_speed
    if camera_last != camera_position:
        camera_last = camera_position.copy()
        map.draw_visible_map(screen, camera_position[1], camera_position[0])
    clock.tick(60)  # limits FPS to 60

pygame.quit()