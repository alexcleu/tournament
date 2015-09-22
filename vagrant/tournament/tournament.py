#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # call PosgreSql
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    # Delete the table matches
    c.execute("DELETE FROM MATCHES")
    DB.commit()
    DB.close()
    


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    # Delete the table players
    c.execute("DELETE FROM PLAYERS")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    # Count the number of players
    c.execute("SELECT COUNT(*) FROM PLAYERS")
    result =  c.fetchall()
    # Turn the result into an integer
    for row in result:
        total_count = row[0]
    DB.close()
    return total_count

    

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    # Insert new player into the table players
    c.execute("INSERT INTO PLAYERS (name) VALUES (%s)",(name,))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    player_ids = []
    # Collect the whole list of players
    c.execute("SELECT player_id from matches")
    for player_id in c.fetchall():
        # Append player_id into the list player_ids
        player_ids.append(player_id[0])
    # Check to see if the player is standing already
    c.execute("SELECT id, name FROM PLAYERS")
    for id, name in c.fetchall():
        # Insert the player_id in matches if it doesn't exists in matches
        if id not in player_ids:
            c.execute("INSERT INTO MATCHES (player_id) VALUES (%s)", (id,))
            DB.commit()
    # Query the returns to check for player statuses
    c.execute(""" SELECT a.id as id,
                         a.name as name,
                         b.wins as wins,
                         b.matches as matches
                  FROM players a
                  JOIN matches b
                  on a.id = b.player_id
                  GROUP BY 1,2,3,4
                  ORDER BY wins DESC      
              """)
    return c.fetchall()
    DB.close()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    # Adds stats for winners
    c.execute("""UPDATE MATCHES
                SET matches = matches + 1, wins = wins +1
                WHERE player_id = (%s)
              """,(winner,))
    DB.commit()
    # Adds stats for losers
    c.execute("""UPDATE MATCHES
                 SET matches = matches + 1 
                 WHERE player_id = (%s)
              """,(loser,))
    DB.commit()
    DB.close

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect()
    c = DB.cursor()
    # Self join in table Matches to find common win id
    c.execute("""
              SELECT c.id1 as id1,
                     d.name as name1,
                     c.id2 as id2,
                     e.name as name2
              FROM(    
              SELECT a.player_id as id1, 
                     b.player_id as id2
              from matches as a, matches as b
              where a.wins = b.wins
              AND a.player_id != b.player_id
              and a.player_id > b.player_id
              ) as c
              JOIN players as d
              on c.id1 = d.id
              JOIN players e
              on c.id2 = e.id
              
              """
              )
    return c.fetchall()

  


