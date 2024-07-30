import math

import pygame
import random

# pygame setup
pygame.init()
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
fps = 60
running = True

rocket_pos = (0, 100)
rocket_pos_vec = pygame.Vector2(rocket_pos[0], rocket_pos[1])

rocket = []
rocket.append(pygame.Surface((30, 30)))

for part in rocket:
    part.set_colorkey((0, 0, 0))
    part.fill("gray")

stars = []
for x in range((screen.get_width() * screen.get_height())/10000):
    star_x = random.randint(0, screen.get_width())
    star_y = random.randint(0, screen.get_height())
    stars.append((star_x, star_y))

# rocket_rect = [x.get_rect() for x in rocket]
# for x in rocket_rect: x.center = (screen.get_width() // 2, screen.get_height() // 2)

rot = 0
rot_speed = 0.0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")
    #pygame.draw.rect(screen, "gray", [(screen.get_width() / 2) - 10, (screen.get_height() / 2) - 10, 20, 20])
    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        rot_speed -= 0.1 * (60/fps)
    if keys[pygame.K_q]:
        rot_speed += 0.1 * (60/fps)
    rot = (rot + rot_speed) % 360
    rocket_image = pygame.transform.rotate(rocket[0], rot)
    rect = rocket_image.get_rect()
    rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    for star in stars:
        star_x = star[0]
        star_y = star[0]
        if star_x > screen.get_width():
            star_x_over = star_x / screen.get_width()
            star_x_over = math.floor(star_x_over)
            star_x = star_x - star_x_over
        elif star_x < 0:
            star_x_over = star_x / screen.get_width()
            star_x_over = math.floor(star_x_over)
            star_x = star_x - star_x_over
        if star_y > screen.get_width():
            star_y_over = star_y / screen.get_width()
            star_y_over = math.floor(star_y_over)
            star_y = star_y - star_x_over
        elif star_y < 0:
            star_y_over = star_y / screen.get_width()
            star_y_over = math.floor(star_y_over)
            star_y = star_y - star_y_over
        pygame.draw(screen, "white", (star_x, star_y), 3)
    screen.blit(rocket_image, rect)
    pygame.display.flip()

    clock.tick(fps)  # limits FPS to 60

pygame.quit()
