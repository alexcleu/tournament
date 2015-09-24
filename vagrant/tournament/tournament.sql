-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


/* SCHEMA */ 
--Drop the database if it exsits
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

--Create table for players
--id: specific id for players
--name: player's name
CREATE TABLE PLAYERS (
	ID serial PRIMARY KEY,
	NAME TEXT
);

--Create table for matches
--id: specific id for matches
--wins: count how many wins, starting from 0
--matches: report how many mathces, starting from 0
--player_id: record the player's status
CREATE TABLE MATCHES(
	ID serial primary key,
	wins int DEFAULT 0,
	matches int DEFAULT 0,
	player_id int references players(id)
);
--Create view to pair two players up				 
CREATE VIEW PAIRING as
    SELECT a.player_id as id1, 
           b.player_id as id2
    from matches as a, matches as b
    where a.wins = b.wins
    AND a.player_id != b.player_id
    and a.player_id > b.player_id
;
--Create a table to record games players had won with out playing
--player_id: player_id of the player that receives a free win
CREATE TABLE FREEWIN(
  player_id int references players(id)
);