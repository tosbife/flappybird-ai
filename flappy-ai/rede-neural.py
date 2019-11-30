import math
import random
from main import play


class Specie():
  def __init__(self, population, max_weight, max_mutation):
    """ Creates individuals with the same neurons properties but with random weights. """
    self.__neurons_count = 3
    self.__max_weight = max_weight
    self.__max_mutation = max_mutation

    self.population = population

    self.generation = 1
    self.scores = [(0, 0)] * self.population
    self.individuals = self.getRandomIndividuals()
    self.individuals[0] = (-0.019633530774151753, 0.016274713018109788, -0.5762916339922682)


  def getRandomIndividuals(self):
    """ Return individuals with random weights. """
    return [
      tuple (
        random.uniform(-self.__max_weight, self.__max_weight)
        for _ in range(self.__neurons_count)
      )
      for _ in range(self.population)
    ]


  def playWithAll(self):
    """ Makes all individuals test their skills. """
    print("Geração Nº", self.generation)
    self.scores = play(self.individuals, self.population, self.generation)
    print(*enumerate(self.scores), sep="\n")


  def repopulate(self, parentsQtt):
    """ Repopulate the specie with 'parentsQtt' number of parents. """
    self.generation += 1    
    parents, highscores = list(self.bestIndividuals(parentsQtt))

    if not parents:
      self.individuals = self.getRandomIndividuals()
    else:
      if highscores[0][0] > 1:
        self.__max_mutation = .1
      for i, parent in enumerate(parents):
        self.individuals[i] = parent      
      for i in range(parentsQtt, self.population):
        self.individuals[i] = self.crossover(parents)
    
    self.scores = [0] * self.population


  def bestIndividuals(self, N):
    """ Returns the 'N' individuals with best scores (0-scored individuals aren't considered). """
    highscores = [[0, -999]] * N
    best_players_indexes = [-1] * N

    # For each score
    for i in range(self.population):
      score = self.scores[i]

      # Defines in wich colocation the current score and player are
      for j in range(N):
        if score > highscores[j]:
          highscores[j] = score
          best_players_indexes[j] = i
          break

    # Return all individuals
    parents = []
    leng = 0
    print("Melhores: ", end="")
    for i in best_players_indexes:
      if i == -1:
        break
      print(i, end=" ")
      parents.append(self.individuals[i])
      leng += 1
    print()
    return parents[:leng], highscores[:leng]

  def crossover(self, parents):
    """ Return a new individual with parents' genes modified. """
    return tuple(
      random.choice(parents)[n]  # random parent's genes
      + random.uniform(-self.__max_mutation, self.__max_mutation)  # random mutation
      for n in range(self.__neurons_count)
    )


specie = Specie(
  population=10,
  max_weight=1,
  max_mutation=.5
)
while True:
  specie.playWithAll()
  specie.repopulate(parentsQtt=2)