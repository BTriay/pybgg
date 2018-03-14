PRAGMA foreign_keys = ON;

create table GAME(
	game_id integer primary key,
	bgg_game_id integer not null,
	name text not null);

create table PLAYER(
	player_id integer primary key,
	name text not null);

create table COLLECTION(
	player_id integer not null,
	game_id integer not null,
	rating integer,
	foreign key (player_id) references PLAYER(player_id) on delete cascade,
	foreign key (game_id) references GAME(game_id) on delete cascade);
