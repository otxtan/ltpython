import gc
import math
import random
import threading
import time
from collections import deque

import pygame
from setuptools.command.alias import alias

from Alien import Alien
from Bullet import Bullet
from Defender import Defender
from Laser import Laser
from pygame import font

# khởi tạo màn hình
screen_width = 1376
screen_height = 860
screen = pygame.display.set_mode((screen_width, screen_height))

alienList = []
bulletShootedList = []
laserShootedList=[]
bulletList = []
font.init()
myfont = pygame.font.SysFont('Arial', 150)
explosion = pygame.image.load('image/explosion2.png')
scaled_explosion = pygame.transform.scale(explosion,(int(explosion.get_width() * 1), int(explosion.get_height() * 1)))
clock = pygame.time.Clock()
rd = int(random.uniform(5,20))
for i in range(rd):
    alien = Alien(random.uniform(0, screen_width), random.uniform(0, screen_height / 3), "image/alienpblog.png", 0.3)
    alien.set_speed(3)  # Đặt tốc độ
    alienList.append([alien, True])
for i in range(rd):
    bullet = Bullet(0, 0, "image/onlyrocket.png", 0.1)
    bullet.set_speed(3)  # Đặt tốc độ
    bulletList.append(bullet)
defender = Defender(0, screen.get_height() - pygame.image.load("image/ship1a_0.png").get_height(),
                    "image/ship1a_0.png", 1, bulletList)
defender.set_speed(5)
maxXDefender = screen.get_width() - defender.width - defender.speed
maxYDefender = screen.get_height() - defender.height + defender.speed

def resetGame():
    alienList.clear()
    bulletShootedList.clear()
    bulletList.clear()
    laserShootedList.clear()
    rd = int(random.uniform(5,20))
    for i in range(rd):
        alien = Alien(random.uniform(0, screen_width), random.uniform(0, screen_height / 3), "image/alienpblog.png",
                      0.5)
        alien.set_speed(3)  # Đặt tốc độ
        alienList.append([alien, True])
    for i in range(rd+1):
        bullet = Bullet(0, 0, "image/onlyrocket.png", 0.1)
        bullet.set_speed(20)  # Đặt tốc độ
        bulletList.append(bullet)


def colideAlien():
    for b in bulletShootedList:
        if b.y<0:
            bulletShootedList.remove(b)
        for a in alienList:
            # print(f'đầu đạn: {b.y}, đuôi đạn:{b.y+b.height} ,.đầu alien:{a[0].x}, đuôi alien:{a[0].x+a[0].height}')
            if b.y<=a[0].y+a[0].height and (b.y+b.height)>=a[0].y and a[0].x<=b.x <= a[0].x+a[0].width:

                screen.blit(scaled_explosion, (a[0].x, a[0].y))

                alienList.remove(a)
                bulletShootedList.remove(b)


                return False
    return True

def colideDefender():

    for l in laserShootedList:
        if l.y>screen_height:
            laserShootedList.remove(l)
        # print(f'{l.y} gia tri {defender.y}')
        if  (l.y <= defender.y+defender.height and (l.y+l.height)>=defender.y) and defender.x <= l.x <= defender.x + defender.width and defender.x <= (l.x+l.width) <= defender.x + defender.width:
            laserShootedList.remove(l)
            text = pygame.font.SysFont('Arial', 150).render("lose", True, (255, 255, 255))
            screen.blit(text, (screen_width/2, screen_height/2))
            return False
    return True


def controlDefender():
    keys = pygame.key.get_pressed()


    if keys[pygame.K_UP] and keys[pygame.K_RIGHT] and defender.x <= maxXDefender and defender.y > 0:
        defender.move_forward_right()

    elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT] and defender.x <= maxXDefender and defender.y < maxYDefender:
        defender.move_backward_right()
    elif keys[pygame.K_UP] and keys[pygame.K_LEFT] and defender.x > 0 and defender.y > 0:
        defender.move_forward_left()
    elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT] and defender.x > 0 and defender.y < maxYDefender:
        defender.move_backward_left()
    elif keys[pygame.K_UP] and defender.y > 0:
        # print(f'x1: {defender.x}, y: {(screen.get_height() - defender.height)}, defender height:{defender.width}')
        defender.move_forward()
    elif keys[pygame.K_DOWN] and defender.y < maxYDefender:
        defender.move_backward()
    elif keys[pygame.K_LEFT] and defender.x > 0:
        defender.move_left()
    elif keys[pygame.K_RIGHT] and defender.x < maxXDefender:
        defender.move_right()
    else:
        defender.set_velocity(0, 0)  # Dừng di chuyển nếu không có phím nào được nhấn
    defender.update()
    defender.render(screen)



def controlAlien(alien,redict):
    if redict == True:
        alien.move_right()
    else:
        alien.move_left()

    alien.update()
    return alien
def bulletAndLaser():
    for bulletShooted in bulletShootedList:
        bulletShooted.move_forward()
        bulletShooted.update()
        bulletShooted.render(screen)
    for laserShooted in laserShootedList:
        laserShooted.move_backward()
        laserShooted.update()
        laserShooted.render(screen)
def controlAliens():
    for group in alienList:
        if group[0].x < 0:
            group[1] = True
        elif group[0].x > screen.get_width() - group[0].width - group[0].speed:
            # , screen.get_height() - group[0].height + group[0].speed
            group[1] = False
        group[0] = controlAlien(group[0], group[1])
        # if defender.x-5<group[0].x<defender.x+5:
        if random.uniform(0, screen.get_width() - group[0].width - group[0].speed) < 3:
            laser=Laser(group[0].x, group[0].y + group[0].height, "image/texture_laser.png", 0.2)
            laser.speed=5
            laserShootedList.append(laser)
        group[0].render(screen)

def run():
    pygame.init()

    image = pygame.image.load('image/onlyrocket.png')
    scaled_image = pygame.transform.scale(image, (int(image.get_width() * 0.1), int(image.get_height() * 0.1)))
    play = pygame.image.load('image/play.png')
    scaled_play = pygame.transform.scale(play, (int(image.get_width() * 0.9), int(image.get_height() * 0.3)))
    image_rect = scaled_play.get_rect()
    image_rect.x = screen_width / 2 - image_rect.width / 2
    image_rect.y = screen_height / 2
    playAgain = True
    win = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(defender.bullets) > 0:
                        bullet = defender.bullets.pop()
                        bullet.x = defender.x + (defender.width / 2) - bullet.width/2
                        bullet.y = defender.y - defender.height
                        bulletShootedList.append(bullet)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Kiểm tra nút chuột trái được nhấn (button = 1)
                    mouse_pos = pygame.mouse.get_pos()  # Lấy vị trí hiện tại của chuột
                    if image_rect.collidepoint(mouse_pos):  # Kiểm tra xem chuột có nằm trong vùng hình ảnh hay không
                        playAgain = False
                        resetGame()

        screen.fill((0, 0, 0))
        if len(bulletList)<1:
            playAgain = True
            win = 2
        if playAgain == False:

            if colideDefender() == False:

                playAgain = True
                win = 2
            elif colideAlien() == False:
                if len(alienList) <= 0:
                    playAgain = True
                    win = 1
            else:
                text = pygame.font.SysFont('Arial', 35).render(str(len(defender.bullets)), True, (255, 255, 255))
                screen.blit(text, (screen_width - 85, 50))
                screen.blit(scaled_image, (screen_width - 50, 50))
                controlDefender()
                controlAliens()
                bulletAndLaser()

        else:
            if win == 1:
                ketqua = 'You Win'
            elif win == 2:
                ketqua = 'You Lose'
            else:
                ketqua = ''
            text = pygame.font.SysFont('Arial', 35).render(ketqua, True, (255, 255, 255))
            screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - 50))
            screen.blit(scaled_play, image_rect)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def main():
    run()


if __name__ == "__main__":
    main()
