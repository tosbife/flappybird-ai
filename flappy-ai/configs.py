import pygame

class Configs:
  """ Basic class to store of all important values/objects. """ 
  screen = game_speed = scores = distance = bottom_pipes = None

  @classmethod
  def resetValues(cls, qtt):
    """ Redefines all non-constant attributes. """
    cls.screen = pygame.display.set_mode((cls.Dimensions.screen_w, cls.Dimensions.screen_h))
    cls.bottom_pipes = list()
    cls.game_speed = 70
    cls.scores = [[0, 0] for _ in range(qtt)]
    cls.distance = 0
  
  @classmethod
  def updateValues(cls, dt, is_any_alive):
    """ Update all static variables. """
    cls.distance += cls.game_speed * dt
    cls.game_speed *= is_any_alive
  
  class Dimensions:
    """ Size-related constants. """
    screen_w = 288
    screen_h = 510
    pipe_gap = 90
    floor_y = 398
    flappy_x = 47
    score = (124, 50)
  
  class Images:
    """ Loaded sprites. """
    sky = pygame.image.load("images/sky.png")
    floor = pygame.image.load("images/base.png")
    
    pipe1 = pygame.image.load("images/pipe.png")
    pipe2 = pygame.transform.flip(pipe1, False, True)

    birds = (
      pygame.image.load("images/bird1.png"),
      pygame.image.load("images/bird2.png"),
      pygame.image.load("images/bird3.png")
    )

  class Text:
    """ Text-related constans. """    
    font = pygame.font.Font('C:\\Users\\Almei\\Desktop\\flappy-ai\\VCR_OSD_MONO_1.001.ttf', 17)
    info_colors = (
      (233, 233, 233),
      (233, 233, 233),
      (255, 255, 255)
    ) 