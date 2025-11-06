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
    pygame.draw.polygon(part, "gray",
                        #((0, 10), (0, 20), (20, 20), (20, 30), (30, 15), (20, 0), (20, 10)))
                        ((0, 15), (10, 15), (10, 30), (20, 30), (20, 15), (30, 15), (15, 0)))

stars = []
for x in range(int((screen.get_width() * screen.get_height())/10000)):
    star_x = random.randint(0, screen.get_width())
    star_y = random.randint(0, screen.get_height())
    stars.append((star_x, star_y))

# rocket_rect = [x.get_rect() for x in rocket]
# for x in rocket_rect: x.center = (screen.get_width() // 2, screen.get_height() // 2)

rot = 0
rot_speed = 0.0
background_offset = [0, 0]
background_offset_speed = [0, 0]

font = pygame.font.Font(pygame.font.match_font('arial'), 16)

def apply_rot(x, y, rot):
    x_new = ((math.cos(rot * math.pi / 180) * x) + (math.sin(rot * math.pi / 180) * y * -1))
    y_new = ((math.cos(rot * math.pi / 180) * y) + (math.sin(rot * math.pi / 180) * x))
    return (x_new, y_new)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")
    #pygame.draw.rect(screen, "gray", [(screen.get_width() / 2) - 10, (screen.get_height() / 2) - 10, 20, 20])
    keys = pygame.key.get_pressed()
    x_speed_add = 0
    y_speed_add = 0
    #TODO: diagnonal keys pressed should only add our "available thrust", not doubled
    available_thrust = 0.1
    thrust_derivative = 0
    for i in [keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]]:
        thrust_derivative += 1
    if not thrust_derivative == 0:
        available_thrust = available_thrust / thrust_derivative
    if keys[pygame.K_e]:
        rot_speed -= 0.05 * (60/fps)
    if keys[pygame.K_q]:
        rot_speed += 0.05 * (60/fps)
    if keys[pygame.K_r]:
        rot_speed -= 0.03 * (60/fps) * rot_speed
    if keys[pygame.K_w]:
        x_speed_add += (60/fps) * available_thrust
    if keys[pygame.K_s]:
        x_speed_add -= (60 / fps) * available_thrust
    if keys[pygame.K_a]:
        y_speed_add += (60 / fps) * available_thrust
    if keys[pygame.K_d]:
        y_speed_add -= (60 / fps) * available_thrust
    speed_add = apply_rot(x_speed_add, y_speed_add, rot)
    background_offset_speed[0] += speed_add[0]
    background_offset_speed[1] += speed_add[1]
    background_offset[0] += background_offset_speed[0]
    background_offset[1] += background_offset_speed[1]
    rot = (rot + rot_speed) % 360
    rocket_image = pygame.transform.rotate(rocket[0], rot)
    rect = rocket_image.get_rect()
    rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    for star in stars:
        star_x = star[0]
        star_y = star[1]
        star_y += background_offset[0]
        star_x += background_offset[1]
        if star_x > screen.get_width():
            star_x_over = star_x / screen.get_width()
            star_x_over = star_x_over - math.floor(star_x_over)
            star_x = (star_x_over * screen.get_width())
        elif star_x < 0:
            star_x_over = star_x / screen.get_width()
            star_x_over = star_x_over - math.floor(star_x_over)
            star_x = (star_x_over * screen.get_width())
        if star_y > screen.get_width():
            star_y_over = star_y / screen.get_width()
            star_y_over = star_y_over - math.floor(star_y_over)
            star_y = (star_y_over * screen.get_width())
        elif star_y < 0:
            star_y_over = star_y / screen.get_width()
            star_y_over = star_y_over - math.floor(star_y_over)
            star_y = (star_y_over * screen.get_width())
        pygame.draw.circle(screen, "white", (star_x, star_y), 3)
    screen.blit(rocket_image, rect)
    position_stats = font.render("Position: x: " + str(int(background_offset[0])) + " (" + ("+" if background_offset_speed[0] > 0 else "") + str(int(background_offset_speed[0]*fps)) + ") y: " + str(int(background_offset[1])) + " (" + ("+" if background_offset_speed[1] > 0 else "") + str(int(background_offset_speed[1]*fps)) + ")", True, "white")
    position_stats_rect = position_stats.get_rect()
    position_stats_rect.topleft = (0, 0)
    screen.blit(position_stats, position_stats_rect)
    rotation_stats = font.render("Rotation: " + str(int(rot)), True, "white")
    rotation_stats_rect = rotation_stats.get_rect()
    rotation_stats_rect.topleft = (0, 16)
    screen.blit(rotation_stats, rotation_stats_rect)
    pygame.display.flip()

    clock.tick(fps)  # limits FPS to 60

pygame.quit()
