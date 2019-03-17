def read_from_file(filename):
	with open(filename, "r") as fi:
		words = fi.read().split('.')[0]
		return words.split()


class hangman_core:
	def __init__(self, filename):
		self.words_list = read_from_file(filename)

	def get_random_word(self):
		import random
		return random.choice(self.words_list)


class hangman_game:
	def __init__(self, word, max_incorrect_guesses=11):
		self.chars_list = dict()
		for i in range(len(word)):
			if word[i] not in self.chars_list:
				self.chars_list[word[i].lower()] = [i]
			else:
				self.chars_list[word[i].lower()].append(i)

		self.word_to_guess = word
		self.guessing_word = ['_'] * len(word)
		self.incorrect_guesses = 0
		self.max_incorrect_guesses = max_incorrect_guesses

	def is_gameover(self):
		return self.incorrect_guesses == self.max_incorrect_guesses

	def __check_guess__(self, char):
		char = char.lower()
		if char not in self.chars_list:
			self.incorrect_guesses += 1
			return False
		else:
			for pos in self.chars_list[char]:
				self.guessing_word = char
			return True

