# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 18:34:12 2022

@author: Cream
"""
import random
from MancalaGamev0 import Board
from MancalaGamev0 import Player

class Queen0(Player):
    
    """ Basic minimax AI
    """
    
    def __init__(self, num, lookahead):
        """ Creates AI """
        self.lookahead = lookahead
        super().__init__(num)
        
    def __repr__(self):
        """ Creates representation of Queen with number
        """
        s = 'Queen as Player ' + str(self.num)
        return s
    
    def best_without_empty_strings(self, scores):
        """ Finds the max or min based on player number
            and ignores empty strings
        """
        scores = [x for x in scores if type(x) == int]
        if self.num == 0:
            m = min(scores)
        else:
            m = max(scores)
        return m
    
    def best_score_row(self, scores, b):
        """ Gives the row with the best score with minimax using the
            specific tiebreak of furthest row from player
        """
        Lis = []
        m = self.best_without_empty_strings(scores)
        for r in range(6):
            if b.slots[r][self.num] != 0 and scores[r] == m:
                Lis += [r]
        if self.num == 0:
            row = Lis[0]
        else:
            row = Lis[-1]
        return row
    
    def scores_for(self, b):
        """ Creates a list with the scores for Queen
            given the input board recursively
        """
        scores = ['' for x in range(6)]
        for r in range(6):
            if b.is_win_for(1):
                score_r = 48
            elif b.is_win_for(0):
                score_r = -48
            elif b.is_tie():
                score_r = 0
            elif b.slots[r][self.num] == 0:
                score_r = ''
            elif self.lookahead == 0:
                score_r = self.queen_score_diff(b)
            else:
                b1 = self.side_move(b, r)
                p = Queen0(b1.p_turn, self.lookahead - 1)
                next_scores = p.scores_for(b1)
                score_r = p.best_without_empty_strings(next_scores)
            scores[r] = score_r
        return scores
    
    def side_move(self, board, row):
        """ Makes the next move on a new board
            and returns the updated board without updating 
            the previous input board or players
        """
        b1 = board.copy()
        p0 = Player(0)
        p1 = Player(1)
        if b1.p_turn == 0:
            p0.turn = True
            p1.turn = False
        else:
            p0.turn = False
            p1.turn = True
        if p0.turn:
            p0.quiet_move(b1, p1, row)
        else:
            p1.quiet_move(b1, p0, row)
        return b1
        
    def next_move(self, b):
        """ Overrides the current next move function
            to have one for Queen instead where
            she picks her best move
        """
        scores = self.scores_for(b)
        r = self.best_score_row(scores, b)
        return r
    
    def queen_score_diff(self, b):
        """ Finds the difference between Player 1's score
            and Player 0's on the current board
        """
        L = [b.mancala_0, b.mancala_1]
        sum_0 = 0
        sum_1 = 0
        for i in range(6):
            sum_0 += b.slots[i][0]
            sum_1 += b.slots[i][1]
        L[0] += sum_0
        L[1] += sum_1
        d = L[1] - L[0]
        return d
                
class RandomPlayer(Player):
    
    def next_move(self, b):
        """ Makes a move function so the random player AI
            just makes random moves
        """
        Lis = [r for r in range(6) if b.slots[r][self.num] != 0]
        r = random.choice(Lis)
        return r                
                
                
                
                
                