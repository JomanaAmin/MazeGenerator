import pygame
class Button:
    def __init__(self,screen,x,y,msg):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 195
        self.height = 30
        self.rect=pygame.Rect(x,y,self.width,self.height) #creates a rectangle surface for button
        self.msg=msg
        self.font=pygame.font.Font("freesansbold.ttf",15) #identify font
        self.text=self.font.render(msg,True,"White","Black") #render some text returns a surface with this text
        self.button=self.text.get_rect(center=(self.rect.center)) #returns a rect object with a center and size same as text surface, that way the text is centered
    def drawButton(self,screen):
        pygame.draw.rect(screen,"Black",self.rect)
        screen.blit(self.text,self.button)

    def isClicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
