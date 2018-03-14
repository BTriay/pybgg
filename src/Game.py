class Game():
	def __init__(self, bgg_game_id):
		self.bgg_game_id = bgg_game_id
		self.name = ''
		self.average = ''
		self.votes = {}
		for i in range(1,11):
			self.votes[i] = list()

	def rating_voters(self, rating):
		"""returns the voters for a particular rating"""
		return self.votes[rating]

	def add_rating(self, rating, voter):
		"""add the rating from a particular voter"""
		try:
			rating = int(round(float(rating)))
			if (0<rating) & (rating<11): #else silently ignore
				self.votes[rating].append(voter)
		except ValueError:
			pass

	def ratings_count(self):
		j=0
		for i in range(1,11):
			j+=len(self.votes[i])
			print('Rating {}: {} voters'.format(i, len(self.votes[i])))
		print('Total number of votes: {}'.format(j))

	def display(self):
		print('Game: {}\nGame id: {}\nAverage: {}\n'.format(self.name, self.game_id, self.average))
		self.ratings_count()

