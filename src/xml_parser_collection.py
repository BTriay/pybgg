import xml.etree.ElementTree as ET
import pickle
import bgg_requests

class CollectionGame():
	def __init__(self, game_id):
		self.game_id = game_id
		self.name = ''
		self.rating = ''	

	def add_name(self, name):
		self.name = name

	def add_rating(self, rating):
		self.rating = rating

	def display(self):
		print('Game: {}\nGame id: {}\nRating: {}\n'.format(self.name, self.game_id, self.rating))

def collection_parser(coll_file_name):
	tree = ET.parse(coll_file_name)
	root = tree.getroot()
	game_list = list()
	for it in root:
		g = CollectionGame(it.attrib['objectid'])
		game_list.append(g)
		for el in it.iter('name'):
			g.add_name(el.text)
		for el in it.iter('rating'):
			g.add_rating(el.attrib['value'])
	return game_list

coll_template = 'coll_template.xml'
game_list = collection_parser(coll_template)

for it in game_list:
	it.display()
