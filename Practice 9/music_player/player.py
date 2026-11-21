
import pygame
import os


class MusicPlayer:
    def __init__(self):
        self.songs = [
            "music/song1.mp3",
            "music/song2.mp3",
            "music/song3.mp3"
        ]

        self.current_song = 0

    def play(self):
        pygame.mixer.music.load(self.songs[self.current_song])
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next_song(self):
        self.current_song += 1

        if self.current_song >= len(self.songs):
            self.current_song = 0

        self.play()

    def previous_song(self):
        self.current_song -= 1

        if self.current_song < 0:
            self.current_song = len(self.songs) - 1

        self.play()
