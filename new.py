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
            if grid[row][col+i] != '.' and grid[row][col+i] != word[i]:
                return False
        else:
            # 纵向放置
            if grid[row+i][col] != '.' and grid[row+i][col] != word[i]:
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
                # 更新 placed_words 列表
                placed_words.append((word, new_row, new_col, new_direction))
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

# 定义一个函数，创造一个wordpuzzle
def create_wordpuzzle(words, rows, cols):
    print(rows,cols)
    # 创建一个空白的grid，用.表示空白格子
    grid = [['.' for _ in range(cols)] for _ in range(rows)]

    # 随机打乱单词列表的顺序
    random.shuffle(words)

    # 定义一个列表，记录已经放入的单词及其位置和方向
    placed_words = []

    word = random.choice(words)
    success, direction, row, col = try_place_word_random(word, grid)
    if success:
        placed_words.append((word, row, col, direction))

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
        # 检查当前状态下是否存在多个解
        # solutions = solve_puzzle(grid[:], words)
        # 打印出 solve_puzzle 函数返回的结果
        # print(f'Solutions found: {len(solutions)}')
        # if len(solutions) < 2:
        #     # 如果没有至少两组解，则撤销上一步操作并尝试其他单词
        #     remove_word(word, grid, row, col, direction)
        #     placed_words.pop()

    # 在grid中随机生成一些#来表示不能填入的地方，并且不会覆盖已经放入的单词（可选）
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '.' and random.random() < 0.05:  # 可以调整概率大小来控制#数量
                grid[i][j] = '#'

    # 返回grid和placed_words列表（用于显示答案）
    return grid, placed_words

# def remove_word(word, grid, row, col, direction):
#     if direction == 0:
#         for i in range(len(word)):
#             grid[row][col+i] = '.'
#     else:
#         for i in range(len(word)):
#             grid[row+i][col] = '.'


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
                if c != '#' and c != '.':
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
                if c != '#' and c != '.':
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
                if puzzle[i][j] == '.':
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
            puzzle[i][j] = '.'

    backtrack(puzzle)
    return solutions



# 定义一个单词列表，可以自行修改或添加
word_list = read_word_list('D:\\Download\\words_alpha.txt')
words = random.sample(word_list, 140)
# ['cat', 'dog', 'rat', 'hat', 'bat', 'mat', 'pat']
# 定义grid的行数和列数，可以自行修改或添加
rows = 15
cols = 15

# 定义一个单词列表，可以自行修改或添加
words = ['cat', 'dog', 'rat', 'hat', 'bat', 'mat', 'pat']
# 定义grid的行数和列数，可以自行修改或添加
# rows = 5
# cols = 5

# 调用create_wordpuzzle函数，传入单词列表和行数列数，得到grid
puzzle, placed_word = create_wordpuzzle(word_list, rows, cols)
# 调用print_grid函数，打印出grid
print('generate')
print_grid(puzzle)
print('placed_word')
print(placed_word)

# solve_puzzle(puzzle, word_list)
