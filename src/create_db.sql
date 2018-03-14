PRAGMA foreign_keys = ON;

create table GAME(
	game_id integer primary key,
	bgg_game_id integer not null,
	name text not null);

create table PLAYER(
	player_id integer primary key,
	name text not null);

create table PLAYER_COLLECTION(
	collection_id integer primary key,
	player_id integer not null,
	foreign key (player_id) references PLAYER(player_id) on delete cascade);

create table COLLECTION(
	collection_id integer not null,
	game_id integer not null,
	foreign key (collection_id) references PLAYER_COLLECTION(collection_id) on delete cascade,
	foreign key (game_id) references GAME(game_id) on delete cascade);

create table PLAYER_RATING(
	player_id integer not null,
	game_id integer not null,
	rating integer not null,
	foreign key (player_id) references PLAYER(player_id) on delete cascade,
	foreign key (game_id) references GAME(game_id) on delete cascade);

