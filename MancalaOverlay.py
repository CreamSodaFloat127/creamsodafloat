# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 00:36:39 2022

@author: Cream
"""

from MancalaGamev3 import Board
from MancalaGamev3 import Player
from MancalaAIv0 import Queen0
from MancalaAIv1 import Queen1
from MancalaAIv0 import RandomPlayer
from MancalaAIv4CopyingQueen1 import Queen4
from MancalaAIv4CopyingQueen1 import Brain
from MancalaAIv4CopyingQueen1 import upload_from_text

def mancala(p0, p1):
    """ Plays Mancala with two player objects
    """
    print('Mancala Time!')
    print()
    b = Board()
    print(b)

    while p0.turn == True or p1.turn == True:
        process_move(p0, p1, b)
    else:
        return b
   
def mancala_middle(p0, p1):
    """ Allows players to start playing in the middle
        of a game that's already started
    """
    b = Board()
    b.assign()
    print(b)
    
    while p0.turn == True or p1.turn == True:
        process_move(p0, p1, b)
    else:
        return b
    
def process_move(p0, p1, b):
    """ Actually process the given move for the player so that
        it knows whether or not to end the game
    """
    if p0.turn:
        p = p0
        other = p1
    else:
        p = p1
        other = p0
    print(str(p) + '\'' + 's turn')
    row = p.next_move(b)
    p.quiet_move(b, other, row)
    print('')
    print(b)
    print(str(p), 'moved row ' + str(row))
    print('')
    if p.check_win(b, other) == True:
        if b.is_win_for(p.num):
            print(str(p), 'wins!')
        elif b.is_win_for(1 - p.num):
            print(str(other), 'wins!')
        else:
            print('It\'s a tie!')
















