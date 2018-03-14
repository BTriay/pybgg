import xml.etree.ElementTree as ET

from Game import Game

def xml_get_game_average(game_file_name):
	tree = ET.parse(game_file_name)
	root = tree.getroot()
	for it in root:
		for el in it.iter('average'):
			return el.attrib['value']

def xml_get_game_name(game_file_name):
	tree = ET.parse(game_file_name)
	root = tree.getroot()
	for it in root:
		for el in it.iter('name'):
			if el.attrib['type'] == 'primary':
				return el.attrib['value']

def xml_get_ratings(game_file_name, game):
	tree = ET.parse(game_file_name)
	root = tree.getroot()
	one_vote = False
	for it in root:
		for el in it.iter('comments'):
			for votes in el:
				one_vote = True
				game.add_rating(votes.attrib['rating'], votes.attrib['username'])
	return one_vote
