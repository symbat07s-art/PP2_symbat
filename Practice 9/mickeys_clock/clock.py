
import pygame
import math
from datetime import datetime


class Clock:
    def __init__(self, screen):
        self.screen = screen

        # Load background
        self.background = pygame.image.load(
            "images/mickeyclock.jpeg"
        ).convert()

        # Load hand images
        hand_image = pygame.image.load(
            "images/minute_hand.png"
        ).convert_alpha()

        # Create hands with different sizes
        self.minute_hand = pygame.transform.scale(
            hand_image, (60, 200)
        )

        self.second_hand = pygame.transform.scale(
            hand_image, (42, 140)
        )

        # Resize background
        self.background = pygame.transform.scale(
            self.background, (800, 600)
        )

    def draw_hand(self, hand, angle, center):
        # Find the pivot point at the bottom of the image
        pivot_x = hand.get_width() / 2
        pivot_y = hand.get_height() * 0.98

        # Rotate the image
        rotated_hand = pygame.transform.rotate(
            hand, -angle
        )

        # Calculate the new position of the pivot
        radians = math.radians(-angle)

        dx = pivot_x - hand.get_width() / 2
        dy = pivot_y - hand.get_height() / 2

        new_x = dx * math.cos(radians) + dy * math.sin(radians)
        new_y = -dx * math.sin(radians) + dy * math.cos(radians)

        # Keep the pivot at the clock center
        hand_rect = rotated_hand.get_rect(
            center=(center[0] - new_x, center[1] - new_y)
        )

        self.screen.blit(rotated_hand, hand_rect)

    def draw(self):
        # Display background
        self.screen.blit(self.background, (0, 0))

        # Get current time
        current_time = datetime.now()

        minutes = current_time.minute
        seconds = current_time.second

        # Calculate angles
        minute_angle = minutes * 6 + seconds * 0.1
        second_angle = seconds * 6

        # Clock center
        center = (400, 300)

        # Draw both hands
        self.draw_hand(self.minute_hand, minute_angle, center)
        self.draw_hand(self.second_hand, second_angle, center)
