#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from contextlib import contextmanager

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # call PosgreSql
    return psycopg2.connect("dbname=tournament")

@contextmanager
def get_cursor():
    """Call out the cursor of the PstgreSQL
    Commit the query if 
    """
    DB = connect()
    c = DB.cursor()
    try:
        yield c
    except:
        raise
    else:
        DB.commit()
    finally:
        c.close()
        DB.close()

def deleteFreeWin():
    """Remove all of the recorded data under free win for odd player"""
    with get_cursor() as c:
        c.execute("DELETE FROM FREEWIN")
    
def deleteMatches():
    """Remove all the match records from the database."""
    # Call delete Freewin method to pass the test script
    deleteFreeWin()
    with get_cursor() as c:
        c.execute("DELETE FROM MATCHES")

def deletePlayers():
    """Remove all the player records from the database."""
    with get_cursor() as c:
        # Delete the players
        c.execute("DELETE FROM PLAYERS")


def countPlayers():
    """Returns the number of players currently registered."""
    with get_cursor() as c:
        # Count the number of players
        c.execute("SELECT COUNT(*) FROM PLAYERS")
        result =  c.fetchone()
        # Turn the result into an integer
        total_count = result[0]
        return total_count
    

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    with get_cursor() as c:
        # Insert new player into the table players
        c.execute("INSERT INTO PLAYERS (name) VALUES (%s)",(name,))


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
    with get_cursor() as c:
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
        # Query the returns to check for player statuses
        c.execute(""" SELECT * 
                      FROM STANDING    
                  """)
        return c.fetchall()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with get_cursor() as c:
        # Adds stats for winners
        c.execute("""UPDATE MATCHES
                     SET matches = matches + 1, wins = wins +1
                     WHERE player_id = (%s)
                  """,(winner,))
        # Adds stats for losers
        c.execute("""UPDATE MATCHES
                     SET matches = matches + 1 
                     WHERE player_id = (%s)
                  """,(loser,))


def oddorEven():
    """Checks whether the players are in odds or evens
    
    Return a TRUE or player_id response
    """
    with get_cursor() as c:
        # Count whether there's odds or even number
        c.execute("""SELECT COUNT(*)
                     FROM MATCHES
                  """)
        for players in c.fetchall():
            total = players[0]
        if total % 2 == 0:
            return "True"        
        else:
            # Free points for the lowest win
            # Check the player hasn't won free point already
            c.execute("""SELECT a.player_id
                         FROM MATCHES a
                         LEFT JOIN FREEWIN b
                         ON a.player_id = b.player_id
                         WHERE b.player_id is NULL
                         ORDER BY WINS ASC
                         LIMIT 1
                      """
                      )
            player_id = c.fetchone()[0]
            # Add points to the odd one
            oddOneFreePoints(player_id)     
            # Return player_id of the odd one
            return player_id
        
def oddOneFreePoints(player_id):
    """ Returns a free point for the odd player
    Arg:
      player_id of the odd one
    
    Returns:
      Free points for the player
    """
    with get_cursor() as c:
        # Add points for the odd one
        c.execute("""UPDATE MATCHES
                     SET wins = wins + 1
                     where player_id = (%s)
                  """,(player_id,
                  ))
        # Add the player that had a free win
        c.execute("""INSERT INTO FREEWIN VALUES (%s)
                  """,(player_id,
                  ))

 
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
    with get_cursor() as c:
        # Check whether the players are odd or even
        Result_oddorEven = oddorEven()
        if Result_oddorEven == "True":
            # self join to get the players matched
            c.execute("""
                      SELECT c.id1 as id1,
                             d.name as name1,
                             c.id2 as id2,
                             e.name as name2
                      FROM(    
                      SELECT id1, 
                             id2
                      FROM pairing
                      ) as c
                      JOIN players as d
                      on c.id1 = d.id
                      JOIN players e
                      on c.id2 = e.id  
                      """
                      )
        else:
            c.execute("""
                      SELECT c.id1 as id1,
                             d.name as name1,
                             c.id2 as id2,
                             e.name as name2
                      FROM(    
                      SELECT id1, 
                             id2
                      FROM pairing
                      ) as c
                      JOIN players as d
                      on c.id1 = d.id
                      JOIN players e
                      on c.id2 = e.id
                      where c.id1 != (%s)
                      and c.id2 != (%s)
                      """
                      ,(Result_oddorEven,Result_oddorEven,))
        return c.fetchall()