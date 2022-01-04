import math
from random import randint, random
from copy import deepcopy


class Chromosome:
    def __init__(self, values):
        self.values = values
        self.__fitness = None

    def __eq__(self, other):
        return self.values == other.values

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return str(self)

    @staticmethod
    def get_random(values_count, target_val):
        return Chromosome(
            [randint(0, target_val) for _ in range(values_count)]
        )

    def calc_fitness(self, coefficients, target_val):
        self.__fitness = 1 / (1 + abs(target_val - sum(k * x for k, x in zip(coefficients, self.values))))
        return self.__fitness

    def get_fitness(self):
        return self.__fitness

    def crossover(self, other):
        cut_point = randint(1, len(self.values))
        return Chromosome(
            self.values[:cut_point] + other.values[cut_point:]
        )

    def mutate(self, target_val):
        mutation_idx = randint(0, len(self.values) - 1)
        self.values[mutation_idx] = randint(0, target_val)


def genetic_search(coefficients, target_val, population_size=100, epochs_limit=0,
                   crossover_chance=0.1, mutation_chance=0.2):
    values_count = len(coefficients)
    population = [Chromosome.get_random(values_count, target_val) for _ in range(population_size)]
    solutions = []
    epoch = 1
    precision = round(math.log10(population_size)) + 1
    while epochs_limit == 0 and len(solutions) < 1 \
            or epoch <= epochs_limit:
        print("Epoch: ", epoch)
        # selection
        total_fitness = 0
        for chromosome in population:
            fitness = chromosome.calc_fitness(coefficients, target_val)
            if fitness == 1 and chromosome not in solutions:
                solutions.append(deepcopy(chromosome))
            total_fitness += fitness
        print("Total fitness: ", round(total_fitness, precision))
        roulette_intervals = []
        cumulative_prob = 0
        for chromosome in population:
            probability = chromosome.get_fitness() / total_fitness
            roulette_intervals.append((cumulative_prob, cumulative_prob + probability))
            cumulative_prob += probability
        selection_probabilities = [random() for _ in range(population_size)]
        selected_elem_indexes = []
        for p in selection_probabilities:
            selected_elem_indexes.append(binary_search(roulette_intervals, 0, population_size - 1, p))
        for i in range(population_size):
            population[i] = population[selected_elem_indexes[i]]
        # crossover
        parents = []
        for i, chromosome in enumerate(population):
            if random() < crossover_chance:
                parents.append((i, chromosome))
        parents_len = len(parents)
        stop = parents_len if parents_len % 2 == 0 else parents_len - 1
        for i in range(0, stop, 2):
            idx = parents[i][0]
            chromosome = parents[i][1]
            population[idx] = chromosome.crossover(parents[i + 1][1])
        if parents_len % 2 != 0:
            idx = parents[parents_len - 1][0]
            chromosome = parents[parents_len - 1][1]
            population[idx] = chromosome.crossover(parents[0][1])
        # mutation
        for chromosome in population:
            if random() < mutation_chance:
                chromosome.mutate(target_val)
        epoch += 1
    return solutions


# find interval where probability falls using a binary search
def binary_search(intervals, left, right, p) -> int:
    if right >= left:
        mid = left + (right - left) // 2
        if intervals[mid][0] <= p < intervals[mid][1]:
            return mid
        elif p < intervals[mid][0]:
            return binary_search(intervals, left, mid - 1, p)
        else:
            return binary_search(intervals, mid + 1, right, p)
    else:
        return -1


def main():
    coefficients = (1, -4, 5, 12, 16)
    target_val = 18
    solutions = genetic_search(coefficients, target_val, 1000)
    print("Found ", len(solutions), " solutions")
    print(solutions)


main()
