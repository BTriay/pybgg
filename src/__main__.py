import logging
import pickle

import bgg_requests as bgg
import xml_parser_game
from Game import Game
import bgg_db

logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(funcName)s: %(message)s')

def get_game_info_basic(game_id):
	game = Game(game_id)

	page_no = 1
	logging.info('Getting info on game %s - processing page %s', game_id, page_no)
	#game_file = bgg.get_game_from_bgg(game.game_id, page_no)
	game_file = './bgg_data/' + str(game.bgg_game_id) + '_page_' + str(page_no) + '.xml'

	game.name = xml_parser_game.xml_get_game_name(game_file)
	game.average = xml_parser_game.xml_get_game_average(game_file)

	game_pickle = 'game_' + str(game.bgg_game_id) + '_basic.dat'
	with open(game_pickle, 'wb') as f:
		pickle.dump(game, f)

	return game_pickle


def get_game_info_inc_ratings(game_id):
	game = Game(game_id)

	page_no = 1
	while True:
		logging.info('Getting info on game %s - processing page %s', game_id, page_no)
		#game_file = bgg.get_game_from_bgg(game.game_id, page_no)
		game_file = './bgg_data/' + str(game.bgg_game_id) + '_page_' + str(page_no) + '.xml'
		if xml_parser_game.xml_get_ratings(game_file, game):
			page_no+=1
		else:
			break

	game.name = xml_parser_game.xml_get_game_name(game_file)
	game.average = xml_parser_game.xml_get_game_average(game_file)

	game_pickle = 'game_' + str(game.bgg_game_id) + '.dat'
	with open(game_pickle, 'wb') as f:
		pickle.dump(game, f)

	return game_pickle

def pickle_game_to_db(game_pickle_file, db_name):
	with open(game_pickle_file, 'rb') as f:
		logging.info('Unpickling the game from %s to %s', game_pickle_file, db_name)
		data = pickle.Unpickler(f)
		game = data.load()
		bgg_db.insert_game(game, db_name)
		game_id = bgg_db.select_from_game_name(game.name, db_name)[0]
		#import pdb; pdb.set_trace()
		for i in range(1, 11):
			for player_name in game.votes[i]:
				bgg_db.insert_rating(player_name, game_id, i, db_name)

def main():
#game_id = 206859 #Iberian rails
#game_id = 126163 #Tzolk'in
#game_id = 164265 #Witness
	db_name = 'bgg.db'
	bgg_db.check_db(db_name)
	#game_pickle_file = get_game_info_inc_ratings(164265)
	game_pickle_file = 'game_164265.dat'
	pickle_game_to_db(game_pickle_file, db_name)

if __name__ == '__main__':
	main()
