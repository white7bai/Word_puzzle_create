import random
from typing import List


class WordPuzzleGA:
    def __init__(self, words: List[str], rows: int, cols: int, pop_size=100, mutation_rate=0.01):
        self.words = words
        self.rows = rows
        self.cols = cols
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.population = [self.random_individual() for _ in range(pop_size)]

    def random_individual(self):
        # Generate a random individual
        return [[random.choice(['.'] + list('abcdefghijklmnopqrstuvwxyz')) for _ in range(self.cols)] for _ in range(self.rows)]

    def fitness(self, individual):
        # Calculate the fitness of an individual
        score = 0
        for row in individual:
            word = ''
            for c in row:
                if c != '.':
                    word += c
                else:
                    if len(word) > 1 and word in self.words:
                        score += len(word)
                        if self.words.count(word) > 1:
                            score += 1
                    word = ''
            if len(word) > 1 and word in self.words:
                score += len(word)
                if self.words.count(word) > 1:
                    score += 1
        for col in zip(*individual):
            word = ''
            for c in col:
                if c != '.':
                    word += c
                else:
                    if len(word) > 1 and word in self.words:
                        score += len(word)
                        if self.words.count(word) > 1:
                            score += 1
                    word = ''
            if len(word) > 1 and word in self.words:
                score += len(word)
                if self.words.count(word) > 1:
                    score += 1
        return score

    def selection(self):
        # Select two individuals from the population using tournament selection
        k = 3
        a = max(random.sample(self.population, k), key=self.fitness)
        b = max(random.sample(self.population, k), key=self.fitness)
        return a, b

    def crossover(self, a, b):
        # Crossover two individuals to generate two offspring
        c = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        d = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < 0.5:
                    c[i][j] = a[i][j]
                    d[i][j] = b[i][j]
                else:
                    c[i][j] = b[i][j]
                    d[i][j] = a[i][j]
        return c, d

    def mutation(self, individual):
        # Mutate an individual with a certain probability
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < self.mutation_rate:
                    individual[i][j] = random.choice(
                        ['.'] + list('abcdefghijklmnopqrstuvwxyz'))

    def run(self, iterations=1000):
        # Run the genetic algorithm for a certain number of iterations
        for i in range(iterations):
            new_population = []
            while len(new_population) < self.pop_size:
                a, b = self.selection()
                c, d = self.crossover(a, b)
                self.mutation(c)
                self.mutation(d)
                new_population.append(c)
                new_population.append(d)
            self.population = new_population
            print(f'Iteration {i}: Best fitness = {self.fitness(self.best_individual())}')

    def best_individual(self):
        # Return the best individual from the population
        return max(self.population, key=self.fitness)


# Example usage
words = ['cat', 'dog', 'rat', 'hat', 'bat', 'mat', 'pat']
rows = 5
cols = 5

ga = WordPuzzleGA(words, rows, cols)
ga.run()

best_individual = ga.best_individual()
for row in best_individual:
    print(' '.join(row))
