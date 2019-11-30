import pygame
import time

pygame.init()
# Game separated objects
from constants import Configs
from flappy import Flappy
from pipe import Pipe, PipesGenerator
from background import MovingBackground


def play(weights, qtt, generation):
  """ Simulates a flappy game with some a.i. controlling all flappys. """
  pygame.init()
  pygame.display.set_caption("flappy")
  Configs.resetValues(qtt)

  # Instantiate objects
  clock = pygame.time.Clock()
  i = -1
  flappys = tuple(
    Flappy(w, (i := i + 1))
    for w in weights
  )
  pipes = pygame.sprite.Group(
    PipesGenerator.returnPipes()
  )
  sky = MovingBackground(
    image=Configs.Images.sky,
    location=(0, 0),
    speed=0.01
  )
  floor = MovingBackground(
    image=Configs.Images.floor,
    location=(0, 400),
    speed=1
  )
  
  # Main loop
  while True:
    # FPS setting
    dt = clock.tick(60) / 1000

    # Objects drawing    
    sky.blitme()
    for pipe in pipes:
      pipe.blitme()
    for flappy in flappys:
      flappy.blitme()
    floor.blitme()
    draw_infos(
      f"Geração: {generation}",
      f"Melhor indivíduo: {Configs.scores.index(max(Configs.scores)) + 1}",
      f"Melhor Score: {int(max(Configs.scores)[0])}"
    )
    pygame.display.flip()

    # Listen to events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        print(*(enumerate(flappy.weight) for flappy in flappys), sep="\n")
    
    # Neural Network input
    isAnyAlive = False
    for flappy in flappys:
      if not flappy.is_done:     
        isAnyAlive = True
      if flappy.is_alive:        
        closest = Configs.bottom_pipes[0]
        args = (
          flappy.rect.bottom - Configs.Dimensions.floor_y,
          closest.rect.left - flappy.rect.right,
          closest.rect.top - flappy.rect.bottom
        )
        flappy.is_up = flappy.needsToFlap(args)
      
      
    # Return verification
    if not isAnyAlive:
        time.sleep(0.5)
        pygame.display.quit()

        return Configs.scores

    # Objects updating
    Configs.updateValues(dt, any(f.is_alive for f in flappys))
    for flappy in flappys:
      flappy.update(dt, pipes)
    pipes.update(dt, flappys)
    floor.update(dt)
    sky.update(dt)

    # Pipes spawning
    if PipesGenerator.isCooldown(dt):
      pipes.add(PipesGenerator.returnPipes())


def draw_infos(*infos):
    """ Draws the current evolutional info into screen with the default font. """
    for y, text in enumerate(infos):
      Configs.screen.blit(
        source=Configs.Text.font.render(text, False, Configs.Text.info_colors[y]),
        dest=(10, 10 + y*20)
      )