import xml.etree.ElementTree as ET
import pickle
import bgg_requests

class CollectionGame():
	def __init__(self, bgg_game_id):
		self.bgg_game_id = bgg_game_id
		self.name = ''
		self.rating = ''	

	def add_name(self, name):
		self.name = name

	def add_rating(self, rating):
		self.rating = rating

	def display(self):
		print('Game: {}\nGame id: {}\nRating: {}\n'.format(self.name, self.bgg_game_id, self.rating))

def collection_parser(file_name):
	tree = ET.parse(file_name)
	root = tree.getroot()
	game_list = list()
	for it in root:
		g = CollectionGame(it.attrib['objectid'])
		game_list.append(g)
		for el in it.iter('name'):
			g.add_name(el.text)
		for el in it.iter('rating'):
			g.add_rating(el.attrib['value'])

	player_name = file_name.split('collection_')[1].split('.xml')[0]
	pickle_file = 'collection_' + str(player_name) + '.dat'
	with open(pickle_file, 'wb') as f:
		pickle.dump(game_list, f)

	return pickle_file
