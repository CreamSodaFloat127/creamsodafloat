# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 00:38:34 2022

@author: Cream
"""

import random
import copy

class Board:
    
    def __init__(self):
        """ Creates board
        """
        self.mancala_1 = 0
        self.mancala_0 = 0
        self.slots = [[4,4] for r in range(6)]
        self.free_turn = False
        self.p_turn = 0
        
    def __repr__(self):
        """ Allows to see board
        """
        s = 'P1: ' + str(self.mancala_1) + '\n'
        for row in range(6):
            s += str(row) + ' |' 
            for col in range(2):
               s += str(self.slots[row][col]) + '|'
            s += '\n'  
        s += '   0 ' + '1' + '\n'
        s += 'P0: ' + str(self.mancala_0)
        return s

    def copy(self):
        """ Makes a copy of a board with no connections
        """
        new_b = Board()
        new_b.mancala_0 = self.mancala_0
        new_b.mancala_1 = self.mancala_1
        new_b.free_turn = self.free_turn
        new_b.p_turn = self.p_turn
        for r in range(6):
            for c in range(2):
                new_b.slots[r][c] = self.slots[r][c]
        return new_b

    def move(self, row, column):
        """ Moves the stones counter clockwise 
            given the row and column according to
            rules of Mancala
        """
        pile = self.slots[row][column]
        edge = False
        r = row
        c = column
        self.slots[r][c] = 0
        while pile > 0:
            if r == 0 and c == 1:
                if column == 1:
                    self.mancala_1 += 1
                    c = 0
                    pile += -1
                    if pile > 0:
                        self.slots[r][c] += 1
                        pile += -1
                    else:
                        edge = True
                        self.free_turn = True
                else:
                    c = 0
                    self.slots[r][c] += 1
                    pile += -1
                        
            elif r == 5 and c == 0:
                if column == 0:
                    self.mancala_0 += 1
                    c = 1
                    pile += -1
                    if pile > 0:
                        self.slots[r][c] += 1
                        pile += -1
                    else:
                        edge = True
                        self.free_turn = True
                else:
                    c = 1
                    self.slots[r][c] += 1
                    pile += -1
                    
            else:
                if c==0:
                    self.slots[r+1][c] += 1
                    r += 1
                    pile += -1
                else:
                    self.slots[r-1][c] += 1
                    r += -1
                    pile += -1
        self.check_capture(r, c, column, edge)
    
    def check_capture(self, r, c, column, edge):
        """ Checks for a capture given the specific
            states of the board
        """            
        if c == column and not edge and self.slots[r][c] == 1 and self.slots[r][1-c] != 0:
            if c == 0:
                self.mancala_0 += self.slots[r][1-c] + 1
            else:
                self.mancala_1 += self.slots[r][1-c] + 1
            self.slots[r][c] = 0
            self.slots[r][1-c] = 0
    
    def is_win_for(self, player_num):
        """ Determines if it's a win for the
            input player number
        """
        m0 = self.mancala_0
        m1 = self.mancala_1
        d = m0 - m1
        if m0 + m1 == 48:
            if player_num == 0 and d > 0:
                return True
            elif player_num == 1 and d < 0:
                return True
        return False
    
    def is_tie(self):
        """ Checks if there's a tie
        """
        if self.mancala_0 == 24 and self.mancala_1 == 24:
            return True
        return False
    
    def assign(self):
        """ Creates a board with specific attributes and turns it into
            the input board
        """
        self.mancala_1 = int(input('Enter mancala_1:'))
        for r in range(6):
            for c in range(2):
                self.slots[r][c] = int(input('Enter slots[' + str(r) + '][' + str(c) + '] = '))
        self.mancala_0 = int(input('Enter mancala_0:'))
        self.p_turn = int(input('Enter p_turn:'))
        
    def random(self):
        """ Takes the board and does a random amount
            of moves between 0 and 15
        """
        r0 = RandomPlayer(0)
        r1 = RandomPlayer(1)
        for n in range(random.choice(range(15))):
            if self.p_turn == 0:
                row = r0.next_move(self)
                r0.quiet_move(self, r1, row)
            else:
                row = r1.next_move(self)
                r1.quiet_move(self, r0, row)
    
class Player:
    
    def __init__(self, num):
        """ Creates a player and assigns their number as zero or one
        """
        self.num = num
        self.turn = True
        
    def __repr__(self):
        """ Tells player number
        """
        return 'Player ' + str(self.num)
    
    def flip(self, other, b):
        """ Flips who's turn it is
        """
        self.turn = not self.turn
        other.turn = not other.turn
        b.p_turn = 1 - b.p_turn
        
    def check_win(self, b, other):
        """ Checks if either player wins and returns
            the boolean value
        """
        sum_0 = 0
        sum_1 = 0
        for i in range(6):
            sum_0 += b.slots[i][0]
            sum_1 += b.slots[i][1]
        if sum_0 == 0 or sum_1 == 0:
            self.end_game(other)
            b.slots = [[0,0] for r in range(6)]
            b.mancala_0 += sum_0
            b.mancala_1 += sum_1
            return True
        return False
                

    def next_move(self, b):
        """ Allows the player to make their move on the board
            by asking for input for row from player
        """
        while True:
            r = int(input('Enter a row: '))
            if r not in range(6):
                print('Try again!')
            elif b.slots[r][self.num] == 0:
                print('Try again!')
            else:
                break
        return r
    
    def end_game(self, other):
        """ Ends the game by setting both players turn
            status to false
        """
        self.turn = False
        other.turn = False
    
    def quiet_move(self, b, other, row):
        """ Makes move without print statements and
            without asking for direct input 
            given the row and other player
        """
        if self.turn == True:
            other.turn = False
            b.p_turn = self.num
            if b.slots[row][self.num] == 0:
                pass
            elif self.num == 0:
                b.move(row, 0)
                if b.free_turn:
                    b.free_turn = False
                else:
                    self.flip(other, b)
            else:
                b.move(row, 1)
                if b.free_turn:
                    b.free_turn = False
                else:
                    self.flip(other, b)
            self.check_win(b, other)
        else:
            pass
        
    def copy(self):
        """ Makes a copy of the player that is not connected
        """
        
        
    def player_score_diff(self, board):
        """ Finds the difference between the input player's score 
             and the other's on the current board
        """
        L = [board.mancala_0, board.mancala_1]
        sum_0 = 0
        sum_1 = 0
        for i in range(6):
            sum_0 += board.slots[i][0]
            sum_1 += board.slots[i][1]
        L[0] += sum_0
        L[1] += sum_1
        difference = L[self.num] - L[1-self.num]
        return difference
    
    def compete1v1(self, other_player):
        """ Takes two Player AI's and has them compete with one another
            and returns the score of the 'self' player
        """
        board = Board()
        while self.check_win(board, other_player)  == False:
            if self.turn:
                row = self.next_move(board)
                self.quiet_move(board, other_player, row)
            else:
                row = other_player.next_move(board)
                other_player.quiet_move(board, self, row)
        else:
            return self.player_score_diff(board)
        
    def compete_both_sides(self, other_player):
        """ Has both players compete1v1 swapping nuumbers
            and returns the average score of the self
            player
        """
        first_score = self.compete1v1(other_player)
        
        
class RandomPlayer(Player):
    
    def next_move(self, b):
        """ Makes a move function so the random player AI
            just makes random moves
        """
        Lis = [r for r in range(6) if b.slots[r][self.num] != 0]
        r = random.choice(Lis)
        return r 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        