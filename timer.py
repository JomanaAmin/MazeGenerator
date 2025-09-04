import pygame
import time
class Timer:
    def __init__(self,limit,screen,x,y):
        self.startTime = 0
        self.limit=limit
        self.x=x
        self.y=y
        self.currentSeconds=limit
        self.font = pygame.font.SysFont("timesnewroman", 25, True)  # Font name is case-insensitive
        self.timerActive=False
        self.timeUp=False
        self.screen=screen
    def resetTimer(self):
        self.currentSeconds=self.limit
        self.timerActive=False
        self.timeUp=False
    def activateTimer(self):
        self.timerActive=True
        self.currentSeconds=self.limit
    def deactivateTimer(self):
        self.timerActive=False

    def drawTimer(self):
        timer_text = self.font.render(f"Time: {self.currentSeconds}s", True, (231, 230, 247))
        text_rect = timer_text.get_rect(center=(self.x, self.y))
        self.screen.blit(timer_text, text_rect)