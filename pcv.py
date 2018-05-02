from pyeasyga.pyeasyga import GeneticAlgorithm
from distances import Distances
from igraph import *


data = [('pear', 50), ('apple', 35), ('banana', 40)]

ga = GeneticAlgorithm(data)

class Caixeiro:
    def __init__(self):
        self.g = Graph.Full(self.n_vertices, directed=False, loops=False)
        for i in self.g.vs():
            i['visited'] = 0

    def fitness (self, individual, data):
        cont = 0
        for i in data:
            if (g.vs[i]['visited'] == 0):
                g.vs[i]['visited'] = 1
                cont += 1
            else:
                reset()
        return cont


if __name__ == '__main__':
    obj = Caixeiro()
    ga.fitness_function = obj.fitness
    ga.run()
    print (ga.best_individual())
