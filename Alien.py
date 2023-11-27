import random

import pygame


class Alien:
    def __init__(self, x, y, image_path, scale):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.width = int(self.image.get_width() * scale)
        self.height = int(self.image.get_height() * scale)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_visible = True
        self.speed = 1

    def update(self):
        self.x += self.velocity_x * self.speed
        self.y += self.velocity_y * self.speed

    def randomize_velocity(self):
        # Tạo ngẫu nhiên các giá trị vận tốc
        self.velocity_x = random.uniform(-1, 1)
        self.velocity_y = random.uniform(-1, 1)
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_velocity(self, velocity_x, velocity_y):
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def set_visibility(self, is_visible):
        self.is_visible = is_visible

    def move_forward(self):
        self.velocity_x = 0
        self.velocity_y = -1

    def move_backward(self):
        self.velocity_x = 0
        self.velocity_y = 1

    def move_left(self):
        self.velocity_x = -1
        self.velocity_y = 0

    def move_right(self):
        self.velocity_x = 1
        self.velocity_y = 0

    def move_forward_right(self):
        self.velocity_x = 1
        self.velocity_y = -1

    def move_backward_right(self):
        self.velocity_x = 1
        self.velocity_y = 1

    def move_forward_left(self):
        self.velocity_x = -1
        self.velocity_y = -1

    def move_backward_left(self):
        self.velocity_x = -1
        self.velocity_y = 1

    def set_speed(self, speed):
        self.speed = speed


