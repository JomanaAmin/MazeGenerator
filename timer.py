import pygame
import time
class Timer:
    def __init__(self,limit,screen,x,y):
        self.startTime = 0
        self.limit=limit
        self.x=x
        self.y=y
        self.font = pygame.font.SysFont("timesnewroman", 25, True)  # Font name is case-insensitive
        self.timeElapsed=0
        self.timerActive=False
        self.timeUp=True
        self.screen=screen
    def startTimer(self):
        self.startTime=time.time()
        self.timerActive=True
    def updateTimer(self):
        self.timeElapsed=time.time()-self.startTime
        if self.timeElapsed>=self.limit:
            self.TimeUp=True
            self.timerActive=False

    def drawTimer(self):
        timer_text = self.font.render(f"Time: {self.timeElapsed:.2f}s", True, "white")
        text_rect = timer_text.get_rect(center=(self.x, self.y))
        self.screen.blit(timer_text, text_rect)