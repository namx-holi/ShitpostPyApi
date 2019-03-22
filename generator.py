
import os
import random


class WordList:
	"""
	A wordlist that allows getting random words
	"""

	@property
	def name(self):
		return self._name


	def __init__(self, full_path):
		self._full_path = full_path
		self._words = []

		# Name is the base filename without extension
		directory, filename = os.path.split(full_path)
		base_filename, ext = os.path.splitext(filename)
		self._name = base_filename

		self.refresh_words()


	def refresh_words(self):
		self._words = []
		with open(self._full_path, "r") as stream:

			# Store each non-empty line
			for line in stream:
				if line.rstrip():
					self._words.append(line.rstrip())


	def choose(self):
		return random.choice(self._words)


class SentenceGenerator:
	"""
	Generates sentences using templates
	"""

	def __init__(self, template_dir):
		self._template_dir = template_dir
		self._wordlists = {}

		self.build_wordlists()


	def build_wordlists(self):
		# Clear existing wordlists
		self._wordlists = {}

		files = os.listdir(self._template_dir)
		for file in files:
			full_path = os.path.join(self._template_dir, file)

			# Don't try to open directories
			if not os.path.isfile(full_path):
				continue

			wordlist = WordList(full_path)
			self._wordlists[wordlist.name] = wordlist


	def generate_sentence(self):
		# Start with the base sentence
		sentence = "%{}%".format("base")

		# Keep updating the sentence by replacing %xxx% with a word from
		# the dictionary called xxx until there are no more %xxx%s.
		still_updating = True
		while still_updating:
			still_updating = False
			for wordlist in self._wordlists.values():
				while "%{}%".format(wordlist.name) in sentence:
					still_updating = True

					# Just replace one occurance so not everything is
					# the same phrase
					sentence = sentence.replace("%{}%".format(wordlist.name),
						wordlist.choose(), 1)

		# We wrap actual words with |s so it's easier to format them.

		# Fixing the hashtags
		words = []
		for word in sentence.split("||"):
			# If the "word" is a hashtag, we want to make it such that
			# it's valid (remove spaces or dashes)
			if word.startswith("#"):
				word = word.replace(" ", "")
				word = word.replace("-", "")

			words.append(word)
		sentence = "||".join(words)

		# Removing the formatting helper characters
		sentence = sentence.replace("%nul%", "")
		sentence = sentence.replace("||", " ").replace("|", "")

		return sentence.strip()


	def generate_sentences(self, n):
		sentences = []
		for _ in range(n):
			sentences.append(self.generate_sentence())
		return sentences


def main():
	s = SentenceGenerator("Words")
	print(s.generate_sentences(5))


if __name__ == "__main__":
	main()
