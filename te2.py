# 导入random模块
import random
from pathlib import Path

# 定义一个类，表示一个单词拼图
class WordPuzzle:
    # 定义一个类属性，表示允许的字母
    ALLOWABLE_CHARACTERS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # 定义一个初始化方法，传入行数、列数、单词列表、掩码和字典文件路径
    def __init__(self, nrows, ncols, wordlist, mask=None, dict_path="/usr/share/dict/american-english"):
        # 把参数赋值给实例属性
        self.nrows = nrows
        self.ncols = ncols
        self.mask = mask
        self.dict_path = dict_path
        # 创建一个空白的grid，用.表示空白格子
        self.grid = [[' ']*ncols for _ in range(nrows)]
        # 定义一个列表，记录已经放入的单词及其位置和方向
        self.placed_words = []
        # 从字典文件中读取单词列表，并转换为小写
        self.words = [word.lower() for word in Path(dict_path).read_text().splitlines()]
        self.wordlist = random.sample(self.words, 10000)
    
    # 定义一个方法，检查一个单词是否可以放入一个位置
    def check_word(self, word, row, col, direction):
        # direction为0表示横向，为1表示纵向
        # 如果单词长度超过了边界，返回False
        if direction == 0 and col + len(word) > self.ncols:
            return False
        if direction == 1 and row + len(word) > self.nrows:
            return False
        if row < 0 or col < 0:
            return False
        # 遍历单词的每个字母，检查是否和已有的字母匹配，或者是否为空白
        for i in range(len(word)):
            if direction == 0:
                # 横向放置
                if self.grid[row][col+i] not in (' ', word[i]):
                    return False
            else:
                # 纵向放置
                if self.grid[row+i][col] not in (' ', word[i]):
                    return False
        # 如果没有冲突，返回True
        return True
    
    # 定义一个方法，将一个单词放入一个位置
    def place_word(self, word, row, col, direction):
        # direction为0表示横向，为1表示纵向
        # 遍历单词的每个字母，将其放入对应的格子
        for i in range(len(word)):
            if direction == 0:
                # 横向放置
                self.grid[row][col+i] = word[i]
            else:
                # 纵向放置
                self.grid[row+i][col] = word[i]
    
    # 定义一个方法，打印出grid
    def print_grid(self):
        # 遍历grid的每一行，用空格连接每个格子，并打印出来
        for row in self.grid:
            print(' '.join(row))
    
    # 定义一个方法，找出两个单词共享的字母和位置
    def find_shared_letter(self, word1, word2):
        set1 = set(word1)
        set2 = set(word2)
        shared_letters = set1 & set2 # 集合交集运算
        for letter in shared_letters:
            return letter, word1.index(letter), word2.index(letter)
        return None
    
    # 定义一个方法，尝试把一个单词放入grid中，与另一个已经放入的单词交叉
    def try_place_word_cross(self, word):
        # 遍历已经放入的单词
        for placed_word, row, col, direction in self.placed_words:
            # 找出两个单词共享的字母和位置
            shared = self.find_shared_letter(word, placed_word)
            # 如果有共享的字母
            if shared:
                letter, i1, i2 = shared
                # 根据已经放入的单词的方向，确定新单词的方向和起始位置
                if direction == 0: # 横向放入
                    new_direction = 1 # 纵向放入
                    new_row = row - i1 # 起始行号为已放入单词所在行减去共享字母在新单词中的位置
                    new_col = col + i2 # 起始列号为已放入单词所在列加上共享字母在已放入单词中的位置
                else: # 纵向放入
                    new_direction = 0 # 横向放入
                    new_row = row + i2 # 起始行号为已放入单词所在行加上共享字母在已放入单词中的位置
                    new_col = col - i1 # 起始列号为已放入单词所在列减去共享字母在新单词中的位置
                # 检查新单词是否可以放入这个位置和方向，如果可以，就放入，并返回True
                if self.check_word(word, new_row, new_col, new_direction):
                    self.place_word(word, new_row, new_col, new_direction)
                    return True, new_direction, new_row, new_col
        # 如果没有找到合适的位置和方向，返回False
        return False, None, None, None
    
    # 定义一个方法，尝试把一个单词随机地放入grid中，不与其他单词交叉
    def try_place_word_random(self, word):
        max_attempts = 10 # 最大尝试次数
        for _ in range(max_attempts):
            # 随机选择一个方向，0为横向，1为纵向
            direction = random.randint(0, 1)
            # 随机选择一个起始位置，row为行号，col为列号
            row = random.randint(0, self.nrows-1)
            col = random.randint(0, self.ncols-1)
            # 检查这个单词是否可以放入这个位置和方向，如果可以，就放入，并返回True
            if self.check_word(word, row, col, direction):
                self.place_word(word, row, col, direction)
                return True, direction, row, col
        # 如果不可以，返回False
        return False, None, None, None
    
    # 定义一个方法，尝试把第一个单词随机地放入grid中，不与其他单词交叉
    def try_place_first_word_random(self, word):
        while True:
            # 随机选择一个方向，0为横向，1为纵向
            direction = random.randint(0, 1)
            # 随机选择一个起始位置，row为行号，col为列号
            row = random.randint(0, self.nrows-1)
            col = random.randint(0, self.ncols-1)
            # 检查这个单词是否可以放入这个位置和方向，如果可以，就放入，并返回True
            if self.check_word(word, row, col, direction):
                self.place_word(word, row, col, direction)
                return True, direction, row, col
        # 如果不可以，返回False
        return False, None, None, None
    
    
    # 定义一个方法，创造一个wordpuzzle
    def create_wordpuzzle(self):
        # 随机打乱单词列表的顺序
        random.shuffle(self.wordlist)

        # 遍历每个单词，尝试将其放入grid中与其他单词交叉或随机地放置
        for word in self.wordlist:
            # 先尝试与其他单词交叉放置，并记录是否成功
            success, direction, row, col = self.try_place_word_cross(word)
            # 如果不成功，再尝试随机地放置，并记录是否成功
            if not success:
                success, direction, row, col = self.try_place_word_random(word)
            # 如果成功，把这个单词及其位置和方向加入到placed_words列表中
            if success:
                self.placed_words.append((word, row, col, direction))

        # 在grid中随机生成一些#来表示不能填入的地方，并且不会覆盖已经放入的单词（可选）
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.grid[i][j] == ' ' and random.random() < 0.05: # 可以调整概率大小来控制#数量
                    self.grid[i][j] = '#'
    
    # 定义一个方法，填充grid中的空白位置为随机字母
    def fill_grid_randomly(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.grid[i][j] == ' ':
                    self.grid[i][j] = random.choice(list(self.ALLOWABLE_CHARACTERS))
    
    # 定义一个方法，移除grid中的掩码，用空白代替
    def remove_mask(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.grid[i][j] == '*':
                    self.grid[i][j] = ' '
    
    # 定义一个方法，从字典中找出两个单词，有两个以上相同位置相同字母，并返回结果
    def find_two_words(self):
        # 定义一个空字典，用来存储每个字母出现的位置
        letter_positions = {}
        # 遍历单词列表中的每个单词
        for word in self.words:
            # 遍历单词中的每个字母
            for i, letter in enumerate(word):
                # 如果字母不在字典中，就创建一个新的键值对
                if letter not in letter_positions:
                    letter_positions[letter] = []
                # 把字母出现的位置添加到字典中
                letter_positions[letter].append((word, i))
        # 遍历单词列表中的每个单词
        for word1 in self.words:
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
                shared_letters, length = self.find_shared_letter_start(word1, word2)
                if shared_letters is not None:
                    return (word1, word2, shared_letters, length)
        # 如果没有找到符合条件的单词对，就返回None
        return None
    
    # 定义一个方法，找出两个单词共享的字母和位置
    def find_shared_letter_start(self, word1, word2):
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
    
    # 定义一个方法，解决拼图，返回所有可能的解决方案
    def solve_puzzle(self):
        solutions = []

        def is_valid():
            # Check if all horizontal and vertical words in the puzzle are valid
            for row in self.grid:
                word = ''
                for c in row:
                    if c != '#' and c != ' ':
                        word += c
                    else:
                        if len(word) > 0 and word not in self.words:
                            return False
                        word = ''
                if len(word) > 0 and word not in self.words:
                    return False
            for col in zip(*self.grid):
                word = ''
                for c in col:
                    if c != '#' and c != ' ':
                        word += c
                    else:
                        if len(word) > 0 and word not in self.words:
                            return False
                        word = ''
                if len(word) > 0 and word not in self.words:
                    return False
            return True

        def find_next_space():
            # Find the next empty space in the puzzle that needs to be filled
            for i in range(self.nrows):
                for j in range(self.ncols):
                    if self.grid[i][j] == ' ':
                        return (i, j)
            return None

        def backtrack():
            space = find_next_space()
            if space is None:
                # All spaces have been filled, so we have found a solution
                solutions.append([row[:] for row in self.grid])
                return
            i, j = space
            for letter in self.ALLOWABLE_CHARACTERS:
                # Try placing each letter in the current space
                self.grid[i][j] = letter
                if is_valid():
                    # If the current state of the puzzle is valid, continue to the next space
                    backtrack()
                # If the current state of the puzzle is not valid or no solution was found,
                # remove the letter from the current space and try a different letter
                self.grid[i][j] = ' '

        backtrack()
        return solutions

# 定义一些参数，比如行数、列数、单词列表、掩码和字典文件路径
nrows = 15
ncols = 15
wordlist = ['cat', 'dog', 'rat', 'hat', 'bat', 'mat', 'pat']
mask = 'circle'
dict_path = "D:\\Download\\words_alpha.txt"

# 创建一个WordPuzzle类的实例，传入参数
wp = WordPuzzle(nrows, ncols, wordlist, mask, dict_path)

# 调用它的create_wordpuzzle方法来生成一个拼图
wp.create_wordpuzzle()

# 调用它的print_grid方法来打印出拼图
wp.print_grid()
