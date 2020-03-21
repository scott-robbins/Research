import datetime
import genetic

gene_set = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.'
target = 'Genetic Algorithms are pretty cool and elegant! Hello GA'


def get_fitness(genes, target):
    return sum(1 for expect, actual in zip(target, genes)
               if expect == actual)


def display(genes, target, start_time):
    dt = datetime.datetime.now() - start_time
    fitness = get_fitness(genes, target)
    print("{}\t{}\t{}".format(genes, fitness, dt))


def make_guess(target):
    start_time = datetime.datetime.now()

    def fnGetFitness(genes):
        return get_fitness(genes, target)

    def fnDisplay(genes):
        display(genes, target, start_time)

    optimalFitness = len(target)
    best = genetic.get_best(fnGetFitness, len(target), optimalFitness, gene_set,fnDisplay)
    return best


print make_guess(target)
