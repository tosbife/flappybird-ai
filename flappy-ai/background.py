import pygame
from constants import Configs

class MovingBackground:
  def __init__(self, location, speed, image):
    self.x = location[0]
    self.y = location[1]
    self.speed = speed
    self.image = image
    self.width = image.get_rect().width
    
  def update(self, dt):
    self.x -= Configs.game_speed * self.speed * dt
    if self.x <= -self.width:
      self.x = 0
  
  def blitme(self):
    Configs.screen.blit(self.image, (self.x, self.y))
    Configs.screen.blit(self.image, (self.x + self.width, self.y))