from math import sqrt
from PIL import Image, ImageDraw, ImageFont
from pyevolve import (G1DList, GSimpleGA, GAllele,
                      Mutators, Crossovers, Consts)
import random
PIL_SUPPORT = True

#Calcula a distancia eucliadiana dos pontos
def cartesian_matrix(coords):
    """ A distance matrix """
    matrix = {}
    for i, (x1, y1) in enumerate(coords):
        for j, (x2, y2) in enumerate(coords):
            dx, dy = x1 - x2, y1 - y2
            dist = sqrt(dx * dx + dy * dy)
            matrix[i, j] = dist
    return matrix

def read_file(arquivo):
    values = []
    for line in arquivo:
        line = line
        line = line.split(" ")
        values.append(line)

    tamanho = values[0]
    tamanho = int(tamanho[0])
    values = values[1:]
    for i in range(0, tamanho):
        values[i] = [int(values[i][0]), int(values[i][1])]
    arquivo.close()
    return values


def tour_length(matrix, tour):
    """ Returns the total length of the tour """
    total = 0
    num_cities = len(tour)
    for i in range(num_cities):
        j = (i + 1) % num_cities
        city_i = tour[i]
        city_j = tour[j]
        total += matrix[city_i, city_j]
    return total


def write_tour_to_img(coords, tour, img_file):
    """ The function to plot the graph """
    padding = 20
    coords = [(x + padding, y + padding) for (x, y) in coords]
    maxx, maxy = 0, 0
    for x, y in coords:
        maxx = max(x, maxx)
        maxy = max(y, maxy)
    maxx += padding
    maxy += padding
    img = Image.new("RGB", (int(maxx), int(maxy)), color=(255, 255, 255))

    font = ImageFont.load_default()
    d = ImageDraw.Draw(img);
    num_cities = len(tour)
    for i in range(num_cities):
        j = (i + 1) % num_cities
        city_i = tour[i]
        city_j = tour[j]
        x1, y1 = coords[city_i]
        x2, y2 = coords[city_j]
        d.line((int(x1), int(y1), int(x2), int(y2)), fill=(0, 0, 0))
        d.text((int(x1) + 7, int(y1) - 5), str(i), font=font, fill=(32, 32, 32))

    for x, y in coords:
        x, y = int(x), int(y)
        d.ellipse((x - 5, y - 5, x + 5, y + 5), outline=(0, 0, 0), fill=(196, 196, 196))
    del d
    img.save(img_file, "PNG")

    print ("The plot was saved into the %s file." % (img_file,))


def G1DListTSPInitializator(genome, **args):
    """ The initializator for the TSP """
    genome.clearList()
    lst = [i for i in range(genome.getListSize())]

    for i in range(genome.getListSize()):
        choice = random.choice(lst)
        lst.remove(choice)
        genome.append(choice)


cm = []
coords = []


def eval_func(chromosome):
    """ The evaluation function """
    global cm
    return tour_length(cm, chromosome)


def main_run():

    global cm, coords

    # load the tsp data file
    filehandle = open("instancias.txt", "r+")
    coords = read_file(filehandle)
    cm = cartesian_matrix(coords)

    # set the alleles to the cities numbers
    setOfAlleles = GAllele.GAlleles(homogeneous=True)
    lst = [i for i in xrange(len(coords))]
    a = GAllele.GAlleleList(lst)
    setOfAlleles.add(a)

    genome = G1DList.G1DList(len(coords))
    genome.setParams(allele=setOfAlleles)

    genome.evaluator.set(eval_func)
    genome.mutator.set(Mutators.G1DListMutatorSwap)
    genome.crossover.set(Crossovers.G1DListCrossoverOX)
    genome.initializator.set(G1DListTSPInitializator)
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(1000)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.03)
    ga.setPopulationSize(80)

    ga.evolve(freq_stats=100)
    best = ga.bestIndividual()

    write_tour_to_img(coords, best, "tsp_result.png")


if __name__ == "__main__":
    main_run()
