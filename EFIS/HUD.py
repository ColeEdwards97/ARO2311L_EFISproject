import math
import pygame
from pygame.locals import *
pygame.init()
import sys


YELLOW = 0xFFFF00

class Dial:

   def __init__(self, image, frameImage, x=0, y=0, w=0, h=0):

       self.x = x 
       self.y = y
       self.image = image
       self.frameImage = frameImage
       self.dial = pygame.Surface( (self.frameImage.get_rect()[2], self.frameImage.get_rect()[3]) )
       self.dial.fill(0xFFFF00)
       if(w==0):
          w = self.frameImage.get_rect()[2]
       if(h==0):
          h = self.frameImage.get_rect()[3]
       self.w = w
       self.h = h
       self.pos = self.dial.get_rect()
       self.pos = self.pos.move(x, y)

   def position(self, x, y):

       self.x = x 
       self.y = y
       self.pos[0] = x 
       self.pos[1] = y 

   def position_center(self, x, y):

       self.x = x
       self.y = y
       self.pos[0] = x - self.pos[2]/2
       self.pos[1] = y - self.pos[3]/2

   def rotate(self, image, angle):

       tmpImage = pygame.transform.rotate(image ,angle)
       imageCentreX = tmpImage.get_rect()[0] + tmpImage.get_rect()[2]/2
       imageCentreY = tmpImage.get_rect()[1] + tmpImage.get_rect()[3]/2

       targetWidth = tmpImage.get_rect()[2]
       targetHeight = tmpImage.get_rect()[3]

       imageOut = pygame.Surface((targetWidth, targetHeight))
       imageOut.fill(0xFFFF00)
       imageOut.set_colorkey(0xFFFF00)
       imageOut.blit(tmpImage,(0,0), pygame.Rect( imageCentreX-targetWidth/2,imageCentreY-targetHeight/2, targetWidth, targetHeight ) )
       return imageOut

   def clip(self, image, x=0, y=0, w=0, h=0, oX=0, oY=0):

       if(w==0):
           w = image.get_rect()[2]
       if(h==0):
           h = image.get_rect()[3]
       needleW = w + 2*math.sqrt(oX*oX)
       needleH = h + 2*math.sqrt(oY*oY)
       imageOut = pygame.Surface((needleW, needleH))
       imageOut.fill(0xFFFF00)
       imageOut.set_colorkey(0xFFFF00)
       imageOut.blit(image, (needleW/2-w/2+oX, needleH/2-h/2+oY), pygame.Rect(x,y,w,h))
       return imageOut

   def overlay(self, image, x, y, r=0):

       x -= (image.get_rect()[2] - self.dial.get_rect()[2])/2
       y -= (image.get_rect()[3] - self.dial.get_rect()[3])/2
       image.set_colorkey(0xFFFF00)
       self.dial.blit(image, (x,y))




class Horizon(Dial):

   def __init__(self, x=0, y=0, w=0, h=0):

       self.image = pygame.image.load('resources/Horizon_GroundSky.png').convert()
       self.frameImage = pygame.image.load('resources/Horizon_Background.png').convert()
       self.maquetteImage = pygame.image.load('resources/Maquette_Avion.png').convert()
       Dial.__init__(self, self.image, self.frameImage, x, y, w, h)
       
   def update(self, screen, angleX, angleY):

       angleX %= 360
       angleY %= 360
       if (angleX > 180):
           angleX -= 360 
       if (angleY > 90)and(angleY < 270):
           angleY = 180 - angleY 
       elif (angleY > 270):
           angleY -= 360
       tmpImage = self.clip(self.image, 0, (59-angleY)*720/180, 250, 250)
       tmpImage = self.rotate(tmpImage, angleX)
       self.overlay(tmpImage, 0, 0)
       #self.overlay(self.frameImage, 0,0)
       self.overlay(self.maquetteImage, 0,0)
       self.dial.set_colorkey(0xFFFF00)
       screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )
       
class Heading(Dial):
    
    def __init__(self, x=0, y=0, w=0, h=0):
    
        self.image = pygame.image.load('resources/HeadingWheel.png').convert()
        self.frameImage = pygame.image.load('resources/HeadingIndicator_Background.png').convert()
        self.indicatorImage = pygame.image.load('resources/HeadingIndicator_Aircraft.png').convert()
        Dial.__init__(self, self.image, self.frameImage, x, y, w, h)
        
    def update(self, screen, angleZ):
    
        angleZ %= 360
        
        tmpImage = self.rotate(self.image, angleZ)
        self.overlay(self.frameImage, 0, 0)
        self.overlay(tmpImage, 0, 0)
        self.overlay(self.indicatorImage, 0, 0)
        self.dial.set_colorkey(0xFFFF00)
        screen.blit( pygame.transform.scale(self.dial, (self.w, self.h)), self.pos )

class Throttle(Dial):

   def __init__(self, x=0, y=0, w=0, h=0):

      self.image = pygame.image.load('resources/ThrottleNeedle.png').convert()
      self.frameImage = pygame.image.load('resources/ThrottleIndicator_Background.png').convert()
      Dial.__init__(self, self.image, self.frameImage, x, y, w, h)

   def update(self, screen, throttle):

      angle = -(throttle * (250/100) + 145)
      tmpImage = self.clip(self.image, 0, 0, 0, 0, 0, -35)
      tmpImage = self.rotate(tmpImage, angle)
      self.overlay(self.frameImage, 0, 0)
      self.overlay(tmpImage, 0, 0)
      self.dial.set_colorkey(0xFFFF00)
      screen.blit( pygame.transform.scale(self.dial, (self.w, self.h)), self.pos )

class Generic(Dial):

   def __init__(self, x=0, y=0, w=0, h=0):

       self.image = pygame.image.load('resources/AirSpeedNeedle.png').convert()
       self.frameImage = pygame.image.load('resources/Indicator_Background.png').convert()
       Dial.__init__(self, self.image, self.frameImage, x, y, w, h)
   def update(self, screen, angleX, iconLayer=0):

       angleX %= 360
       angleX = 360 - angleX
       tmpImage = self.clip(self.image, 0, 0, 0, 0, 0, -35)
       tmpImage = self.rotate(tmpImage, angleX)
       self.overlay(self.frameImage, 0,0)
       if iconLayer:
          self.overlay(iconLayer[0],iconLayer[1],iconLayer[2])
       self.overlay(tmpImage, 0, 0)
       self.dial.set_colorkey(0xFFFF00)
       screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )






        
        
