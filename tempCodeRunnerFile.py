# 导入random模块
import random

# 定义一个函数，检查一个单词是否可以放入一个位置


def check_word(word, grid, row, col, direction):
    # direction为0表示横向，为1表示纵向
    # 如果单词长度超过了边界，返回False
    if direction == 0 and col + len(word) > len(grid[0]):
        return False
    if direction == 1 and row + len(word) > len(grid):
        return False
    if row < 0 or col < 0:
        return False
    # 遍历单词的每个字母，检查是否和已有的字母匹配，或者是否为空白
    for i in range(len(word)):
        if direction == 0:
            # 横向放置
            if grid[row][col+i] != '@' and grid[row][col+i] != word[i]:
                return False
        else:
            # 纵向放置
            if grid[row+i][col] != '@' and grid[row+i][col] != word[i]:
                return False
    # 如果没有冲突，返回True
    return True

# 定义一个函数，将一个单词放入一个位置


def place_word(word, grid, row, col, direction):
    # direction为0表示横向，为1表示纵向
    # 遍历单词的每个字母，将其放入对应的格子
    for i in range(len(word)):
        if direction == 0:
            # 横向放置
            grid[row][col+i] = word[i]
        else:
            # 纵向放置
            grid[row+i][col] = word[i]

# 定义一个函数，打印出grid


def print_grid(grid):
    # 遍历grid的每一行，用空格连接每个格子，并打印出来
    for row in grid:
        print(' '.join(row))


# 定义一个函数，找出两个单词共享的字母和位置
def find_shared_letter(word1, word2):
    set1 = set(word1)
    set2 = set(word2)
    shared_letters = set1 & set2  # 集合交集运算
    for letter in shared_letters:
        return letter, word1.index(letter), word2.index(letter)
    return None

# 定义一个函数，尝试把一个单词放入grid中，与另一个已经放入的单词交叉


def try_place_word_cross(word, grid, placed_words):
    # 定义一个默认的方向
    direction = 0
    # 遍历已经放入的单词
    for placed_word, row, col, direction in placed_words:
        # 找出两个单词共享的字母和位置
        shared = find_shared_letter(word, placed_word)
        # 如果有共享的字母
        if shared:
            letter, i1, i2 = shared
            # 根据已经放入的单词的方向，确定新单词的方向和起始位置
            if direction == 0:  # 横向放入
                new_direction = 1  # 纵向放入
                new_row = row - i1  # 起始行号为已放入单词所在行减去共享字母在新单词中的位置
                new_col = col + i2  # 起始列号为已放入单词所在列加上共享字母在已放入单词中的位置
            else:  # 纵向放入
                new_direction = 0  # 横向放入
                new_row = row + i2  # 起始行号为已放入单词所在行加上共享字母在已放入单词中的位置
                new_col = col - i1  # 起始列号为已放入单词所在列减去共享字母在新单词中的位置
            # 检查新单词是否可以放入这个位置和方向，如果可以，就放入，并返回True
            if check_word(word, grid, new_row, new_col, new_direction):
                place_word(word, grid, new_row, new_col, new_direction)
                return True,  new_direction, new_row, new_col
    # 如果没有找到合适的位置和方向，返回False
    return False, None, None, None

# 定义一个函数，尝试把一个单词随机地放入grid中，不与其他单词交叉


def try_place_word_random(word, grid):
    nrows = rows
    ncols = cols
    max_attempts = 10  # 最大尝试次数
    for _ in range(max_attempts):
        # 随机选择一个方向，0为横向，1为纵向
        direction = random.randint(0, 1)
        # 随机选择一个起始位置，row为行号，col为列号
        row = random.randint(0, nrows-1)
        col = random.randint(0, ncols-1)
        # 检查这个单词是否可以放入这个位置和方向，如果可以，就放入，并返回True
        if check_word(word, grid, row, col, direction):
            place_word(word, grid, row, col, direction)
            # placed_words.append((word, row, col, direction)) # 更新 placed_words 列表
            return True, direction, row, col
        # 如果不可以，返回False
    return False, None, None, None

# 定义一个函数，尝试把第一个单词随机地放入grid中，不与其他单词交叉


def try_place_first_word_random(word, grid):
    nrows = rows
    ncols = cols
    while True:
        # 随机选择一个方向，0为横向，1为纵向
        direction = random.randint(0, 1)
        # 随机选择一个起始位置，row为行号，col为列号
        row = random.randint(0, nrows-1)
        col = random.randint(0, ncols-1)
        # 检查这个单词是否可以放入这个位置和方向，如果可以，就放入，并返回True
        if check_word(word, grid, row, col, direction):
            place_word(word, grid, row, col, direction)
            # placed_words.append((word, row, col, direction)) # 更新 placed_words 列表
            return True, direction, row, col
        # 如果不可以，返回False
    return False, None, None, None

# 定义一个函数，创造一个wordpuzzle

def has_empty_space(grid, rows, cols):
  # 遍历网格中的每个格子
  count = 0
  for i in range(rows):
    for j in range(cols):
      # 如果有空位，
      if grid[i][j] == '@':
        count += 1
        if count/(rows*cols) > 0.03:
                return True
  # 如果没有空位，就返回False
  return False

def create_wordpuzzle(words, rows, cols, first):
    print(rows, cols)
    # 创建一个空白的grid，用.表示空白格子
    grid = [['@' for _ in range(cols)] for _ in range(rows)]

    # 随机打乱单词列表的顺序
    random.shuffle(words)

    # 定义一个列表，记录已经放入的单词及其位置和方向
    placed_words = []

    word = random.choice(words)
    first = first
    success, direction, row, col = try_place_first_word_random(first, grid)

    while has_empty_space(grid, rows, cols):
        word = random.choice(words)
        success, direction, row, col = try_place_word_cross(
            word, grid, placed_words)
        # 打印出当前尝试放入的单词和结果
        # print(f'Trying to place word: {word}')
        # print(f'Cross placement result: {success}')
        # 如果不成功，再尝试随机地放置，并记录是否成功
        if not success:
            success, direction, row, col = try_place_word_random(word, grid)
            # 打印出随机放置的结果
            # print(f'Random placement result: {success}')
        # 如果成功，把这个单词及其位置和方向加入到placed_words列表中
        if success:
            placed_words.append((word, row, col, direction))

        # 在grid中随机生成一些#来表示不能填入的地方，并且不会覆盖已经放入的单词（可选）
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '@':  # 可以调整概率大小来控制#数量
                grid[i][j] = '#'
#     for i in range(rows):
#         for j in range(cols):
#             if grid[i][j] == '@':  # 可以调整概率大小来控制#数量
#                 grid[i][j] = '.'
    return grid, placed_words

    # 遍历每个单词，尝试将其放入grid中与其他单词交叉或随机地放置

    for word in words:
        # 先尝试与其他单词交叉放置，并记录是否成功
        success, direction, row, col = try_place_word_cross(
            word, grid, placed_words)
        # 打印出当前尝试放入的单词和结果
        print(f'Trying to place word: {word}')
        print(f'Cross placement result: {success}')
    # 如果不成功，再尝试随机地放置，并记录是否成功
    if not success:
        success, direction, row, col = try_place_word_random(word, grid)
        # 打印出随机放置的结果
        print(f'Random placement result: {success}')
    # 如果成功，把这个单词及其位置和方向加入到placed_words列表中
    if success:
        placed_words.append((word, row, col, direction))

    # 在grid中随机生成一些#来表示不能填入的地方，并且不会覆盖已经放入的单词（可选）
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '@' and random.random() < 0.05:  # 可以调整概率大小来控制#数量
                grid[i][j] = '#'

    # 返回grid和placed_words列表（用于显示答案）
    return grid, placed_words


def read_word_list(file_path):
    with open(file_path, 'r') as f:
        word_list = [line.strip() for line in f.readlines()]
    return word_list


def solve_puzzle(puzzle, words):
    solutions = []

    def is_valid(puzzle):
        # Check if all horizontal and vertical words in the puzzle are valid
        for row in puzzle:
            word = ''
            for c in row:
                if c != '#' and c != '@':
                    word += c
                else:
                    if len(word) > 0 and word not in words:
                        return False
                    word = ''
            if len(word) > 0 and word not in words:
                return False
        for col in zip(*puzzle):
            word = ''
            for c in col:
                if c != '#' and c != '@':
                    word += c
                else:
                    if len(word) > 0 and word not in words:
                        return False
                    word = ''
            if len(word) > 0 and word not in words:
                return False
        return True

    def find_next_space(puzzle):
        # Find the next empty space in the puzzle that needs to be filled
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] == '@':
                    return (i, j)
        return None

    def backtrack(puzzle):
        space = find_next_space(puzzle)
        if space is None:
            # All spaces have been filled, so we have found a solution
            solutions.append([row[:] for row in puzzle])
            return
        i, j = space
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            # Try placing each letter in the current space
            puzzle[i][j] = letter
            # 打印出当前状态和结果
            print(f'Current state:')
            print_grid(puzzle)
            print(f'Is valid: {is_valid(puzzle)}')
            if is_valid(puzzle):
                # If the current state of the puzzle is valid, continue to the next space
                backtrack(puzzle)
            # If the current state of the puzzle is not valid or no solution was found,
            # remove the letter from the current space and try a different letter
            puzzle[i][j] = '@'

    backtrack(puzzle)
    return solutions

def sort_words(wordlist):
    # 定义一个空字典，用来存储排序后的单词和原始的单词
    sorted_words = {}
    # 遍历单词列表中的每个单词
    for word in wordlist:
        # 把单词转换为小写字母，并按照字母顺序排序
        sorted_word = "".join(sorted(word.lower()))
        # 如果排序后的单词已经在字典中，就把原始的单词添加到对应的值列表中
        if sorted_word in sorted_words:
            sorted_words[sorted_word].append(word)
        # 如果排序后的单词不在字典中，就创建一个新的键值对，值为一个只包含原始单词的列表
        else:
            sorted_words[sorted_word] = [word]
        # print(sorted_words)
    print(sorted_words)
    # 返回字典
    return sorted_words


def find_two_words(wordlist):
    # 定义一个空字典，用来存储每个字母出现的位置
    letter_positions = {}
    # 遍历单词列表中的每个单词
    for word in wordlist:
        # 遍历单词中的每个字母
        for i, letter in enumerate(word):
            # 如果字母不在字典中，就创建一个新的键值对
            if letter not in letter_positions:
                letter_positions[letter] = []
            # 把字母出现的位置添加到字典中
            letter_positions[letter].append((word, i))
    # 遍历单词列表中的每个单词
    for word1 in wordlist:
        # 定义一个集合，用来存储与word1有相同位置相同字母的单词
        shared_words = set()
        # 遍历word1中的每个字母
        for i, letter in enumerate(word1):
            # 如果字典中有这个字母，就遍历这个字母出现的所有位置
            if letter in letter_positions:
                for word2, j in letter_positions[letter]:
                    # 如果word2和word1不同，并且字母出现在相同位置，就把word2添加到集合中
                    if word2 != word1 and i == j:
                        shared_words.add(word2)
        # 遍历集合中的所有单词
        for word2 in shared_words:
            # 如果word1和word2至少有两个位置相同字母，就返回这一对单词和它们共享的所有字母和位置
            shared_letters, length = find_shared_letter_start(word1, word2)
            if shared_letters is not None:
                return (word1, word2, shared_letters, length)
    # 如果没有找到符合条件的单词对，就返回None
    return None

def find_shared_letter_start(word1, word2):
    # 定义一个空字符串，用来存储共享的字母和位置
    shared = ''
    # 遍历两个单词中较短的那个单词的每个字母
    min_len = min((len(word1), len(word2)))
    max_len = max((len(word1), len(word2)))
    for i in range(min_len):
        # 如果两个单词在同一位置有相同的字母，就把它们加入到字符串中
        if word1[i] == word2[i]:
            shared += word1[i]
        else:
            shared += '.'
    # 如果字符串中有两个或以上的非.字符，就返回字符串，否则返回None
    if shared.count('.') <= len(shared) - 2:
        for i in range(max_len - min_len):
            shared += '.'
        return shared,len(shared)
    else:
        return None, None


def read_word_list(file_path):
    with open(file_path, 'r') as f:
        word_list = [line.strip() for line in f.readlines()]
    return word_list

# 定义一个单词列表，可以自行修改或添加
word_list = read_word_list('D:\\Download\\words_alpha.txt')
words = random.sample(word_list, 1400)
# ['cat', 'dog', 'rat', 'hat', 'bat', 'mat', 'pat']
# 定义grid的行数和列数，可以自行修改或添加

random.shuffle(word_list)
# 调用上面的函数，把每个单词按照字母顺序排序，并存储到一个字典中
# sorted_words = sort_words(word_list)
# 调用上面的函数，从字典中找到两个单词，有两个以上相同位置相同字母，并打印结果
result = find_two_words(word_list)
if result:
        print("Two words that have two or more same letters in the same positions are:",
        result[0], "and", result[1])
        print("The shared letters and positions are:", result[2])
        print("The length is", result[3])
else:
        print("No such words found.")
        

rows = 15
cols = 15

# 定义一个单词列表，可以自行修改或添加
words = ['cat', 'dog', 'rat', 'hat', 'bat', 'mat', 'pat']
# 定义grid的行数和列数，可以自行修改或添加
# rows = 5
# cols = 5
# first = '@@@@@@us@@'
first = result[2]
# 调用create_wordpuzzle函数，传入单词列表和行数列数，得到grid
puzzle, placed_word = create_wordpuzzle(word_list, rows, cols, first)
# 调用print_grid函数，打印出grid
print('generate')
print_grid(puzzle)
print('placed_word')
print(placed_word)
