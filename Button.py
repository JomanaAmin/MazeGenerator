import pygame
class Button:
    def __init__(self,screen,x,y,msg,wid):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = wid
        self.height = 30
        self.rect=pygame.Rect(x,y,self.width,self.height) #creates a rectangle surface for button
        self.msg=msg

        self.baseColor=(231, 230, 247)
        self.hoverColor=(198, 210, 237)
        self.clickColor=(172, 183, 208)
        self.currentColor=self.baseColor
        self.textColor=(130, 112, 129)

        self.font=font = pygame.font.SysFont("timesnewroman", 17,True)  # Font name is case-insensitive
        self.text=self.font.render(msg,True,self.textColor) #render some text returns a surface with this text
        self.button=self.text.get_rect(center=self.rect.center) #returns a rect object with a center and size same as text surface, that way the text is centered

    def drawButton(self,screen):
        pygame.draw.rect(screen,self.currentColor,self.rect, border_radius=15)
        screen.blit(self.text,self.button)

    def isClicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    def update(self, eventList):
        mousePos=pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            self.currentColor=self.hoverColor
            for event in eventList:
                if event.type == pygame.MOUSEBUTTONDOWN :
                    self.currentColor=self.clickColor

        else:
            self.currentColor=self.baseColor

