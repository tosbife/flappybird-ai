import pygame
from abc import ABCMeta, abstractclassmethod
from constants import Configs
from random import randint


class PipesGenerator:
  cooldown = 0

  @classmethod
  def isCooldown(cls, dt):
    cls.cooldown -= dt
    return cls.cooldown < 0
  
  @classmethod
  def returnPipes(cls):
    cls.cooldown = 3
    ry = randint(40, 260)
    return TopPipe(ry), BottomPipe(ry)


class Pipe(pygame.sprite.Sprite, metaclass=ABCMeta):
  """ Abstract class for bottom and top pipes. """

  def __init__(self):
    super().__init__()

    # General attributes
    self.is_in_front = True
    self.x = Configs.Dimensions.screen_w
  
  def update(self, dt, flappys):
    """ Updates it's position and removes itself when outside of screen. """
    self.x -= Configs.game_speed * dt
    self.rect.x = self.x
    
    if self.rect.right <= 0:
      self.kill()
    
  def blitme(self):
    """ Draws it on screen. """
    Configs.screen.blit(self.image, (self.x, self.rect.y))


class BottomPipe(Pipe):
  def __init__(self, y):
    """ Creates a non-flipped pipe. """
    super().__init__()

    # Visual attributes
    self.rect = pygame.rect.Rect(
      (self.x, y + Configs.Dimensions.pipe_gap),  # Location
      (52, 320)                                   # Dimensions
    )
    self.image = Configs.Images.pipe1
    
    # Adds it to pipes-that-flappy-can-see list
    Configs.bottom_pipes.append(self)

  def update(self, dt, flappys):
    """ Updates it's position. """
    super().update(dt, flappys)

    # Removes itself from pipes-that-flappy-can-see group
    for i, flappy in enumerate(flappys):
      if self.is_in_front and self.rect.right <= Configs.Dimensions.flappy_x:
        Configs.bottom_pipes.remove(self)
        Configs.scores[i][0] +=1 
        self.is_in_front = False


class TopPipe(Pipe):
  def __init__(self, y):
    """ Creates a flipped pipe. """
    super().__init__()

    # Visual attributes
    self.rect = pygame.rect.Rect(
      (self.x, y-320), # Location
      (52, 320)        # Dimensions
    )
    self.image = Configs.Images.pipe2