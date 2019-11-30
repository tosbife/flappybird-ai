import pygame
import math
from constants import Configs
from pipe import BottomPipe

class Flappy:
  def __init__(self, neurons, i):
    """ Creates an instance of Flappy. """
    # Apresentation
    print(f"{i} -> {neurons}")
    
    # Neural Network related variables
    self.neurons = neurons
    self.i = i

    # General variables
    self.is_alive = True
    self.is_done = False
    
    # Sprites managment
    self.img_i = 0
    self.img_time = .12
    self.angle = 0

    # Physical attributes
    self.rect = pygame.rect.Rect(
      (Configs.Dimensions.flappy_x,
       Configs.Dimensions.screen_h * .5),  # Location
      (34, 22)                             # Dimension      
    )
    self.vsp = 0
    self.grv = 25
    self.jumpf = -300
    self.is_up = False
  
  def update(self, dt, pipes):
    """ Updates flappy's position and sprite """
    # On floor verification
    if self.is_done:
      self.rect.x -= dt * Configs.game_speed
      return
    
    # Vertical velocity
    self.vsp += self.grv * dt
    # Jumping verification
    if self.is_up and self.is_alive:
      self.vsp = self.jumpf * dt
      self.is_up = False
    # Actually moving
    self.rect.y += self.vsp

    # Collision with floor
    if self.rect.collidepoint(self.rect.x, Configs.Dimensions.floor_y):
      self.is_done = True
      self.is_alive = False
      return

    # Image rotation
    self.angle = -self.vsp * 2 ** (self.vsp < 0)
    # Death verification
    if not self.is_alive:
      return
    
    # Collision with pipes or sky
    if self.rect.bottom < 0 or any(self.rect.colliderect(p.rect) for p in pipes):
      self.is_alive = False
      self.vsp = 0
      bp = Configs.bottom_pipes[0].rect
      Configs.scores[self.i][1] = - ((bp.left - self.rect.right)**2 + (bp.top - self.rect.bottom) ** 2) ** .5
      if (score := Configs.scores[self.i])[0] == 0:
        score[0] = self.rect.left / bp.right

    # Sprite updating
    if (t := self.img_time - dt) <= 0:
      t = .12 - t
      if (i := self.img_i + 1) == 3:
        i = 0
      self.img_i = i
    self.img_time = t
    

  def needsToFlap(self, args):
    """ Defines wether flappy needs to flappy or not depending on enviroment and it's neurons. """
    s = sum(self.neurons[i] * args[i] for i in range(3))
    
    try:
      out = 1 / (1 + math.exp(-s))
      return out > .5
    except OverflowError:
      return False
    

  def blitme(self):
    """ Draws it on screen. """
    image = pygame.transform.rotate(Configs.Images.birds[self.img_i], self.angle)
    Configs.screen.blit(image, self.rect)