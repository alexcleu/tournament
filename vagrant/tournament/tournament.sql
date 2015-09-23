-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


/* SCHEMA */ 

CREATE TABLE PLAYERS (
	ID serial PRIMARY KEY,
	NAME TEXT,
);

CREATE TABLE MATCHES(
	ID serial primary key,
	wins int DEFAULT 0,
	matches int DEFAULT 0,
	player_id references players(id),
);
					 
CREATE VIEW PAIRING as
    SELECT a.player_id as id1, 
           b.player_id as id2
    from matches as a, matches as b
    where a.wins = b.wins
    AND a.player_id != b.player_id
    and a.player_id > b.player_id
;

CREATE TABLE FREEWIN(
  player_id int references players(id)
);