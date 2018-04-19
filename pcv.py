from pyeasyga.pyeasyga import GeneticAlgorithm
from distances import Get_distances

data = [('pear', 50), ('apple', 35), ('banana', 40)]

ga = GeneticAlgorithm(data)


def fitness (individual, data):
    fitness = 0
    if individual.count(1) == 2:
        for (selected, (fruit, profit)) in zip(individual, data):
            if selected:
                fitness += profit
    return fitness


ga.fitness_function = fitness
ga.run()
print ga.best_individual()
