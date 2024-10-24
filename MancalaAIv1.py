# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 18:34:12 2022

@author: Cream
"""
import random
from MancalaGamev3 import Board
from MancalaGamev3 import Player

class Queen1(Player):
    
    """ Alpha-Beta Pruning AI
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
    
    def scores_for(self, board):
        """ Creates the scores for Queen on an 
            input board by calling the minimax function
        """
        scores = ['' for x in range(6)]
        for r in range(6):
            if board.slots[r][self.num] != 0:
                next_board = self.side_move(board, r)
                next_player = Queen1(next_board.p_turn, self.lookahead - 1)
                score_r = next_player.minimax(next_board, -100, 100)[0]
                scores[r] = score_r
        return scores
    
    def minimax(self, board, alpha, beta):
        """ Finds the evaluation of the
            board for Queen given the input board
            recursively using alpha-beta pruning
        """
        row = 0
        if board.is_win_for(1):
            score = 48
        elif board.is_win_for(0):
            score = -48
        elif board.is_tie():
            score = 0
        elif self.lookahead == 0:
            score = self.queen_score_diff(board)
        else:
            if self.num == 0:
                min_score_row = 100
                for r in range(6):
                    if board.slots[r][self.num] != 0:
                        board_next = self.side_move(board, r)
                        p = Queen1(board_next.p_turn, self.lookahead - 1)
                        score_r = p.minimax(board_next, alpha, beta)[0]
                        if score_r < min_score_row:
                            min_score_row = score_r
                            row = r
                        beta = min(beta, score_r)
                    if alpha >= beta:
                        break
                score = min_score_row
            else:
                max_score_row = -100
                for r in range(5,-1,-1):
                    if board.slots[r][self.num] != 0:
                        board_next = self.side_move(board, r)
                        p = Queen1(board_next.p_turn, self.lookahead - 1)
                        score_r = p.minimax(board_next, alpha, beta)[0]
                        if score_r > max_score_row:
                            max_score_row = score_r
                            row = r
                        alpha = max(alpha, score_r)
                    if alpha >= beta:
                        break
                score = max_score_row
        return [score, row]
    
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
        
    def next_move(self, board):
        """ Returns the best move for Queen based on
            what the minimax function returns
        """
        score_and_row = self.minimax(board, -48, 48)
        row = score_and_row[1]
        return row
    
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
                
                
                
                
                