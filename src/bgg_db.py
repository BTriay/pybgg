import pickle
import sqlite3
import logging
import os.path

from Game import Game

fk = 'PRAGMA foreign_keys = ON'

def check_db(db_name):
	"""make sure the db exists and if not, create it"""
	if not os.path.isfile(db_name):
		logging.info('Creating the database %s', db_name)
		with open(db_name, 'w'):
			pass
		conn = sqlite3.connect(db_name)
		cur = conn.cursor()
		db_file = 'create_db.sql'
		with open(db_file, 'r') as f:
			queries = f.read()
			cur.executescript(queries)
		conn.commit()
		conn.close()

# *************************** player-related queries ***************************
def select_player_name(player_id, db_name):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute('select name from player where player_id = ?', (player_id,))
#does not check whether the results is None: player_id will be coming from another table, so *must* exist
	result = cur.fetchone()[0]
	conn.close()
	return result

def select_player_id(player_name, db_name):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute('select player_id from player where name = ?', (player_name,))
	row = cur.fetchone()
	conn.close()
	if row==None:
		return 0
	else:
		return row[0]

def insert_player(player_name, db_name):
	logging.info('Inserting the player %s', player_name)
	player_id = select_player_id(player_name, db_name)
	if player_id==0:
		conn = sqlite3.connect(db_name)
		cur = conn.cursor()
		cur.execute('insert into player (name) values (?)', (player_name,))
		conn.commit()
		conn.close()
	return select_player_id(player_name, db_name)

def insert_game_players_bulk(game, db_name):
	logging.info('Inserting all players who rated the game %s', game.name)
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	for i in range(1,11):
		for player_name in game.votes[i]:
			player_id = select_player_id(player_name, db_name)
			if player_id==0:
				cur.execute('insert into player (name) values (?)', (player_name,))
	conn.commit()
	conn.close()

# *************************** game-related queries ***************************
def select_from_game_name(game_name, db_name):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute('select * from game where name = ?', (game_name,))
	row = cur.fetchone()
	conn.close()
	return row

def select_from_bgg_game_id(bgg_game_id, db_name):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute('select * from game where bgg_game_id = ?', (bgg_game_id,))
	row = cur.fetchone()
	conn.close()
	return row

def insert_game(game_name, bgg_game_id, db_name):
	name_count = select_from_game_name(game_name, db_name)
	id_count = select_from_bgg_game_id(bgg_game_id, db_name)
	if (name_count!=None) | (id_count!=None):
		logging.info('Game %s or game_id %s already in the DB', game_name, bgg_game_id)
		return

	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	logging.info('Inserting the game %s', game_name)
	cur.execute('insert into game (bgg_game_id, name) values (?,?)', (bgg_game_id, game_name))
	conn.commit()
	conn.close()

# *************************** collection-related queries ***************************
def insert_game_rating_single(player_id, game_id, rating, db_name):
	if rating=='N/A':
		rating=-1
	logging.info('Inserting rating %s from %s for the game_id %s', rating, player_id, game_id)

	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute('select player_id, game_id from collection where player_id=? and game_id=?', (player_id, game_id))
	row = cur.fetchone()

	if row==None:
		cur.execute('insert into collection (player_id, game_id, rating) values (?, ?, ?)', (player_id, game_id, rating))

	conn.commit()
	conn.close()

def insert_game_rating_bulk(game, db_name):
	logging.info('Inserting bulk rating for the game "%s"', game.name)

	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	game_id = select_from_bgg_game_id(game.bgg_game_id, db_name)[0]

	for i in range(1,11):
		for player_name in game.votes[i]:
			player_id = select_player_id(player_name, db_name)
			cur.execute('select player_id, game_id from collection where player_id=? and game_id=?', (player_id, game_id))
			row = cur.fetchone()
			if row==None:
				logging.info('Inserting rating %s for the game "%s", player %s', i, game.name, player_name)
				cur.execute('insert into collection (player_id, game_id, rating) values (?, ?, ?)', (player_id, game_id, i))

	conn.commit()
	conn.close()

def insert_game_players_ratings(game, db_name):
	insert_game_players_bulk(game, db_name)
	insert_game_rating_bulk(game, db_name)

def insert_collection(pickle_collection_file, db_name):
	import pdb; pdb.set_trace()
	player_name = pickle_collection_file.split('collection_')[1].split('.dat')[0]
	player_id = insert_player(player_name, db_name)

	with open(pickle_collection_file, 'rb') as f:
		data = pickle.Unpickler(f)
		collection_list = data.load()

		for game in collection_list:
			insert_game(game.name, game.bgg_game_id, db_name)
			game_id = select_from_game_name(game.name, db_name)[0]
			insert_game_rating_single(player_id, game_id, game.rating, db_name)
