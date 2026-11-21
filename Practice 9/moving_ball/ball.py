import pygame


class Ball:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.radius = 25
        self.speed = 20
        self.color = (255, 0, 0)

    def move(self, direction, screen_width, screen_height):
        if direction == "LEFT" and self.x - self.radius >= self.speed:
            self.x -= self.speed

        elif direction == "RIGHT" and self.x + self.radius + self.speed <= screen_width:
            self.x += self.speed

        elif direction == "UP" and self.y - self.radius >= self.speed:
            self.y -= self.speed

        elif direction == "DOWN" and self.y + self.radius + self.speed <= screen_height:
            self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
