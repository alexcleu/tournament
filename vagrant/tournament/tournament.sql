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
)
					 
	