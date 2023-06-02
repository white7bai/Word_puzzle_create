# simulated annealing
import math
import random
from typing import List

class WordPuzzleSA:
    def __init__(self, words: List[str], rows: int, cols: int, unwritable: List[List[bool]]):
        self.words = words
        self.rows = rows
        self.cols = cols
        self.unwritable = [[random.random() < 0.07 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current = self.random_individual()
        self.best = self.current
        self.solutions = [] # a list to store all the better solutions


    def random_individual(self):
        # Generate a random individual
        individual = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if self.unwritable[i][j]:
                    row.append('#')
                else:
                    row.append(random.choice(['.'] + list('abcdefghijklmnopqrstuvwxyz')))
            individual.append(row)
        return individual
        return [[random.choice(['.'] + list('abcdefghijklmnopqrstuvwxyz')) for _ in range(self.cols)] for _ in range(self.rows)]

    def energy(self, individual):
        # Calculate the energy of an individual
        score = 0
        blanks = 0 # count the number of blanks in the grid
        letters = set() # store the letters in the grid
        for row in individual:
            word = ''
            for c in row:
                if c != '.':
                    word += c
                    letters.add(c) # add the letter to the set
                else:
                    blanks += 1 # increase the blank count
                    if len(word) > 1 and word in self.words:
                        score -= len(word)
                    word = ''
            if len(word) > 1 and word in self.words:
                score -= len(word)
        for col in zip(*individual):
            word = ''
            for c in col:
                if c != '.':
                    word += c
                else:
                    if len(word) > 1 and word in self.words:
                        score -= len(word)
                    word = ''
            if len(word) > 1 and word in self.words:
                score -= len(word)
                # modify the score by adding some factors
                score += blanks * 0.1 # add a small positive value for each blank
                score += (26 - len(letters)) * 0.01 # add a smaller positive value for each missing letter
        return score

    def move(self):
        # Generate a new individual by making a small change to the current individual
        new_individual = [row[:] for row in self.current]
        i = random.randrange(self.rows)
        j = random.randrange(self.cols)
        new_individual[i][j] = random.choice(['.'] + list('abcdefghijklmnopqrstuvwxyz'))
        return new_individual

    def run(self, iterations=100000, initial_temperature=1.0, cooling_rate=0.995, max_solutions=10):
        temperature = initial_temperature
        solutions = 0
        for i in range(iterations):
            new_individual = self.move()
            current_energy = self.energy(self.current)
            new_energy = self.energy(new_individual)
            if new_energy < current_energy or random.random() < math.exp((current_energy - new_energy) / temperature):
                self.current = new_individual
                if new_energy < self.energy(self.best):
                    self.best = new_individual
                    self.solutions.append(self.best) # add the better solution to the list
                    solutions += 1
                    if solutions >= max_solutions:
                        break
            temperature *= cooling_rate


# Example usage
words = ['star', 'mars', 'moon', 'soon', 'noon', 'room', 'boom']
# ['cat', 'dog', 'rat', 'hat', 'bat', 'mat', 'pat']
rows = 8
cols = 8

def read_word_list(file_path):
    with open(file_path, 'r') as f:
        word_list = [line.strip() for line in f.readlines()]
    return word_list


# 定义一个单词列表，可以自行修改或添加
word_list = read_word_list('D:\\Download\\words_alpha.txt')

# generate a puzzle with multiple solutions
max_tries = 10 # set a maximum number of tries
tries = 0 # count the number of tries
while tries < max_tries:
 sa = WordPuzzleSA(word_list, rows, cols, unwritable=[]) # create a simulated annealing object
 sa.run(iterations=5000, initial_temperature=10.0, cooling_rate=0.99, max_solutions=10)
 # run the simulated annealing algorithm with max_solutions=2
 if len(sa.solutions) > 1: # if there are more than one solution
    break # break the loop
 else: # if there is only one solution or no solution
    tries += 1 # increase the try count
# sa = WordPuzzleSA(words, rows, cols, unwritable=[])
# sa.run()

best_individual = sa.best
for row in best_individual:
    print(' '.join(row))

# print the number of solutions
print(f'Found {len(sa.solutions)} solutions.')

# print the energy of each solution
for i, solution in enumerate(sa.solutions):
 print(f'Energy of solution {i+1}: {sa.energy(solution)}')

for solution in sa.solutions:
# print the solution
    for row in solution:
        print(' '.join(row))
    print()
