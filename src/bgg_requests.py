import requests
import logging
import time

def get_game_from_bgg(game_id, page):
	logging.info('Requesting page %s for game_id %s', page, game_id)
	msg = 'https://www.boardgamegeek.com/xmlapi2/thing?id=%s&stats=1&ratingcomments=1&page=%s&pagesize=100' % (game_id, page)
	r = requests.get(msg)
	file_name = save_game_xml(game_id, page, r.text)
	return file_name

def save_game_xml(game_id, page, text):
	logging.info('Saving xml page %s for game_id %s', page, game_id)
	file_name = './bgg_data/%s_page_%s.xml' % (game_id, page)
	with open(file_name, 'w') as f:
		f.write(text)
	return file_name

def get_collection_from_bgg(player_name):
	logging.info('Requesting collection for the player %s', player_name)
	msg = 'https://www.boardgamegeek.com/xmlapi2/collection?username=%s&stats=1' % (player_name)
	while True:
		r = requests.get(msg)
		if r.status_code==202:
			logging.info('Sleeping while bgg gets the data')
			time.sleep(5)
		else:
			break
	file_name = save_collection_xml(player_name, r.text)
	return file_name

def save_collection_xml(player_name, text):
	logging.info('Saving xml for %s collection', player_name)
	file_name = './bgg_data/collection_%s.xml' % (player_name)
	with open(file_name, 'w') as f:
		f.write(text)
	return file_name

