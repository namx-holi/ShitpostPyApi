
import os



class SentenceGenerator:
	"""
	Generates sentences using templates
	"""

	def __init__(self, template_dir):
		"""
		Constructor

		@Params
		template_dir : Directory containing templates
		"""

		self._template_dir = template_dir
		self._wordlists = {}

		self.build_wordlists()


	def build_wordlists(self):
		"""
		Builds the wordlists using the template dir
		"""

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
