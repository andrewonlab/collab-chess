#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import json
import math
import copy
from itertools import count
from collections import Counter, OrderedDict, namedtuple


# Our board is represented as a 120 character string. The padding allows for
# fast detection of moves that don't stay within the board.
A1, H1, A8, H8 = 91, 98, 21, 28
initial = (
    '         \n'  #   0 -  9
    '         \n'  #  10 - 19
    ' rnbqkbnr\n'  #  20 - 29
    ' pppppppp\n'  #  30 - 39
    ' ........\n'  #  40 - 49
    ' ........\n'  #  50 - 59
    ' ........\n'  #  60 - 69
    ' ........\n'  #  70 - 79
    ' PPPPPPPP\n'  #  80 - 89
    ' RNBQKBNR\n'  #  90 - 99
    '         \n'  # 100 -109
    '          '   # 110 -119
)

###############################################################################
# Move and evaluation tables
###############################################################################

N, E, S, W = -10, 1, 10, -1
directions = {
    'P': (N, 2*N, N+W, N+E),
    'N': (2*N+E, N+2*E, S+2*E, 2*S+E, 2*S+W, S+2*W, N+2*W, 2*N+W),
    'B': (N+E, S+E, S+W, N+W),
    'R': (N, E, S, W),
    'Q': (N, E, S, W, N+E, S+E, S+W, N+W),
    'K': (N, E, S, W, N+E, S+E, S+W, N+W)
}

pst = {
    'P': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 198, 198, 198, 198, 198, 198, 198, 198, 0,
        0, 178, 198, 198, 198, 198, 198, 198, 178, 0,
        0, 178, 198, 198, 198, 198, 198, 198, 178, 0,
        0, 178, 198, 208, 218, 218, 208, 198, 178, 0,
        0, 178, 198, 218, 238, 238, 218, 198, 178, 0,
        0, 178, 198, 208, 218, 218, 208, 198, 178, 0,
        0, 178, 198, 198, 198, 198, 198, 198, 178, 0,
        0, 198, 198, 198, 198, 198, 198, 198, 198, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'B': (
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 797, 824, 817, 808, 808, 817, 824, 797, 0,
        0, 814, 841, 834, 825, 825, 834, 841, 814, 0,
        0, 818, 845, 838, 829, 829, 838, 845, 818, 0,
        0, 824, 851, 844, 835, 835, 844, 851, 824, 0,
        0, 827, 854, 847, 838, 838, 847, 854, 827, 0,
        0, 826, 853, 846, 837, 837, 846, 853, 826, 0,
        0, 817, 844, 837, 828, 828, 837, 844, 817, 0,
        0, 792, 819, 812, 803, 803, 812, 819, 792, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'N': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 627, 762, 786, 798, 798, 786, 762, 627, 0,
        0, 763, 798, 822, 834, 834, 822, 798, 763, 0,
        0, 817, 852, 876, 888, 888, 876, 852, 817, 0,
        0, 797, 832, 856, 868, 868, 856, 832, 797, 0,
        0, 799, 834, 858, 870, 870, 858, 834, 799, 0,
        0, 758, 793, 817, 829, 829, 817, 793, 758, 0,
        0, 739, 774, 798, 810, 810, 798, 774, 739, 0,
        0, 683, 718, 742, 754, 754, 742, 718, 683, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'R': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'Q': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'K': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 60098, 60132, 60073, 60025, 60025, 60073, 60132, 60098, 0,
        0, 60119, 60153, 60094, 60046, 60046, 60094, 60153, 60119, 0,
        0, 60146, 60180, 60121, 60073, 60073, 60121, 60180, 60146, 0,
        0, 60173, 60207, 60148, 60100, 60100, 60148, 60207, 60173, 0,
        0, 60196, 60230, 60171, 60123, 60123, 60171, 60230, 60196, 0,
        0, 60224, 60258, 60199, 60151, 60151, 60199, 60258, 60224, 0,
        0, 60287, 60321, 60262, 60214, 60214, 60262, 60321, 60287, 0,
        0, 60298, 60332, 60273, 60225, 60225, 60273, 60332, 60298, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
}


###############################################################################
# Chess logic
###############################################################################

class Position(namedtuple('Position', 'board score wc bc ep kp')):
    """ A state of a chess game
    board -- a 120 char representation of the board
    score -- the board evaluation
    wc -- the castling rights
    bc -- the opponent castling rights
    ep - the en passant square
    kp - the king passant square
    """

    def genMoves(self):
        # For each of our pieces, iterate through each possible 'ray' of moves,
        # as defined in the 'directions' map. The rays are broken e.g. by
        # captures or immediately in case of pieces such as knights.
        for i, p in enumerate(self.board):
            if not p.isupper(): continue
            for d in directions[p]:
                for j in count(i+d, d):
                    q = self.board[j]
                    # Stay inside the board
                    if self.board[j].isspace(): break
                    # Castling
                    if i == A1 and q == 'K' and self.wc[0]: yield (j, j-2)
                    if i == H1 and q == 'K' and self.wc[1]: yield (j, j+2)
                    # No friendly captures
                    if q.isupper(): break
                    # Special pawn stuff
                    if p == 'P' and d in (N+W, N+E) and q == '.' and j not in (self.ep, self.kp): break
                    if p == 'P' and d in (N, 2*N) and q != '.': break
                    if p == 'P' and d == 2*N and (i < A1+N or self.board[i+N] != '.'): break
                    # Move it
                    yield (i, j)
                    # Stop crawlers from sliding
                    if p in ('P', 'N', 'K'): break
                    # No sliding after captures
                    if q.islower(): break

    def rotate(self):
        return Position(
            self.board[::-1].swapcase(), -self.score,
            self.bc, self.wc, 119-self.ep, 119-self.kp)

    def move(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]
        put = lambda board, i, p: board[:i] + p + board[i+1:]
        # Copy variables and reset ep and kp
        board = self.board
        wc, bc, ep, kp = self.wc, self.bc, 0, 0
        score = self.score + self.value(move)
        # Actual move
        board = put(board, j, board[i])
        board = put(board, i, '.')
        # Castling rights
        if i == A1: wc = (False, wc[1])
        if i == H1: wc = (wc[0], False)
        if j == A8: bc = (bc[0], False)
        if j == H8: bc = (False, bc[1])
        # Castling
        if p == 'K':
            wc = (False, False)
            if abs(j-i) == 2:
                kp = (i+j)//2
                board = put(board, A1 if j < i else H1, '.')
                board = put(board, kp, 'R')
        # Special pawn stuff
        if p == 'P':
            if A8 <= j <= H8:
                board = put(board, j, 'Q')
            if j - i == 2*N:
                ep = i + N
            if j - i in (N+W, N+E) and q == '.':
                board = put(board, j+S, '.')
        # We rotate the returned position, so it's ready for the next player
        return Position(board, score, wc, bc, ep, kp).rotate()

    def value(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]
        # Actual move
        score = pst[p][j] - pst[p][i]
        # Capture
        if q.islower():
            score += pst[q.upper()][j]
        # Castling check detection
        if abs(j-self.kp) < 2:
            score += pst['K'][j]
        # Castling
        if p == 'K' and abs(i-j) == 2:
            score += pst['R'][(i+j)//2]
            score -= pst['R'][A1 if j < i else H1]
        # Special pawn stuff
        if p == 'P':
            if A8 <= j <= H8:
                score += pst['Q'][j] - pst['P'][j]
            if j == self.ep:
                score += pst['P'][j+S]
        return score






###############################################################################
# User interface
###############################################################################

# Python 2 compatability
if sys.version_info[0] == 2:
    input = raw_input


def parse(c):
    fil, rank = ord(c[0]) - ord('a'), int(c[1]) - 1
    return A1 + fil - 10*rank


def render(i):
    rank, fil = divmod(i - A1, 10)
    return chr(fil + ord('a')) + str(-rank + 1)

#changing the user move to accomodate for the board flipping
def moveSwitch(crdn):
    rdn = []
    if crdn[0] == 'a':
        rdn.append('h')
    elif crdn[0] == 'b':
        rdn.append('g')
    elif crdn[0] == 'c':
        rdn.append('f')
    elif crdn[0] == 'd':
        rdn.append('e')
    elif crdn[0] == 'h':
        rdn.append('a')
    elif crdn[0] == 'g':
        rdn.append('b')
    elif crdn[0] == 'f':
        rdn.append('c')
    elif crdn[0] == 'e':
        rdn.append('d')

    if crdn[1] == '1':
        rdn.append('8')
    elif crdn[1] == '2':
        rdn.append('7')
    elif crdn[1] == '3':
        rdn.append('6')
    elif crdn[1] == '4':
        rdn.append('5')
    elif crdn[1] == '5':
        rdn.append('4')
    elif crdn[1] == '6':
        rdn.append('3')
    elif crdn[1] == '7':
        rdn.append('2')
    elif crdn[1] == '8':
        rdn.append('1')

    return rdn

#Creating two lists that contain the three-part tuples of the pieces for the JSON
def searchBoard(board):
    #tuples for the white team
    teamWhite = []
    #tuples for the black team
    teamBlack = []
    #variable to determine if a king has been killed
    kings = 0
    #starting spot where the pieces are stored in the sting of the board
    start = 21
    #goes through the entire board
    while start < 99:
        #will store a single piece tuple
        temp = []
        #if the spot on the board does not contain a piece
        if board[start] == '.' or board[start] == '\n' or board[start] == ' ':
            start = start + 1
        #if there is a piece in this spot on the black team
        elif board[start] == 'p' or board[start] == 'r' or board[start] == 'b' or board[start] == 'k' or board[start] == 'q' or board[start] == 'n':
            #y-coordinate of the space
            temp.append((math.floor(start/10))-2)
            #x-coordinate of the spot
            temp.append((start%10)-1)
            #the letter of the piece
            if board[start] == 'n':
                temp.append('h')
            else:
                temp.append(board[start])
            #add this tuple to the list for team black
            teamBlack.append(temp)
            start = start + 1
        #piece is on the white team
        else:
            #y-coordinate of the piece
            temp.append((math.floor(start/10))-2)
            #x-coordinate of the piece
            temp.append((start%10)-1)
            #have to change the letter of the piece to lower case
            if (board[start] == 'P'):
                temp.append('p')
            elif (board[start] == 'K'):
                temp.append('k')
            elif (board[start] == 'Q'):
                temp.append('q')
            elif (board[start] == 'B'):
                temp.append('b')
            elif (board[start] == 'N'):
                temp.append('h')
            elif (board[start] == 'R'):
                temp.append('r')
            #put this tuple into list for white team
            teamWhite.append(temp)
            start = start + 1
        #count the number of kings on the board
        if board[start] == 'k' or board[start] == 'K':
            kings = kings + 1
    #return the lists and the number of kings
    return teamBlack, teamWhite, kings

def isCheck(pos):

    temp = copy.deepcopy(pos)
    for moves in temp.genMoves():
        temp = temp.move(moves)
        unused1, unused2, kings = searchBoard(temp.board)
        if (kings < 2):
            return False
        temp = copy.deepcopy(pos)
    return True

def gameOverCheck(pos, tw, tb, redstale, bluestale, k, turn):
    enough = 0
    """
    inCheck = False
    isCheckMate = False
    check = []
    temp = copy.deepcopy(pos)
    for moves in temp.rotate().genMoves():
        temp = temp.rotate().move(moves)
        unused1, unused2, kings = searchBoard(temp.board)
        if (kings < 2):

            inCheck = True
            temp1 = copy.deepcopy(temp)
            for possMoves in temp.genMoves():
                temp1 = temp1.move(possMoves)
                if isCheck(temp1, tw, tb, redstale, bluestale) == False:
                    check.append("F")
                else:
                    check.append("D")
                temp1 = copy.deepcopy(temp)
        temp = copy.deepcopy(pos)
    if "F" not in check and "D" in check:
        print("checkmate")
    """
    if k < 2:
        if turn == True:
            return 2
        else:
            return 1

    if(None not in redstale and None not in bluestale):
        if(redstale[0]==redstale[1] and redstale[0]==redstale[2]):
            if(bluestale[0]==bluestale[1] and bluestale[0]==bluestale[2]):
                return 3

    if(len(tb)<3 and len(tw)<3):
        for piece in tb:
            if(piece[2]!='k' and piece[2]!='p' and piece[2]!='b' and piece[2]!='h'):
                enough = 1
        for piece in tw:
            if(piece[2]!='K' and piece[2]!='P' and piece[2]!='B' and piece[2]!='H'):
                enough = 1
        if(enough == 0):
            return 3
    '''
    temp = copy.deepcopy(pos)
    if isCheck(temp.rotate()) == True:
        print("not check")
        temp2 = copy.deepcopy(pos)
        temp3 = copy.deepcopy(pos)
        for moves in temp2.genMoves():
            temp3.move(moves)
            if isCheck(temp3.rotate()) == True:
                print("not stale")
                return 0
            temp3.copy.deepcopy(pos)
            '''
    return 0


def main():


    #run indefinitely
    while True:
        #initial board
        pos = Position(initial, 0, (True,True), (True,True), 0, 0)
        tb, tw, k = searchBoard(pos.board)

        #write the json file
        with open('board.json', 'w') as file:
            json.dump({'black': tb, 'white': tw, 'over':0}, file, sort_keys=True, indent=4, separators=(',', ': '))

        red = []
        blue = []
        redstale = []
        bluestale = []
        #fill the last three moves with none
        for x in range(0,3):
            redstale.append(None)
            bluestale.append(None)




        #run until a team wins
        while True:
            # We add some spaces to the board before we print it.
            # That makes it more readable and pleasing.
            ' '.join(pos.board)

            # We query the user until she enters a legal move.
            move = None
            while move not in pos.genMoves():
                crdn = input()
                move = parse(crdn[0:2]), parse(crdn[2:4])

            #make the move
            pos = pos.move(move)
            tb, tw, k = searchBoard(pos.rotate().board)
            red.append(move)
            if(len(red) != 2):
                redstale.append(red)
                redstale = redstale[1:]
                red = []
            ov = gameOverCheck(pos, tw, tb, redstale, bluestale, k, True)
            if ov != 0:
                break

            #write json of new board
            with open('board.json', 'w') as file:
                json.dump({'black': tb, 'white': tw, 'over':ov}, file, sort_keys=True, indent=4, separators=(',', ': '))

            # After our move we rotate the board and print it again.
            # This allows us to see the effect of our move.
            ' '.join(pos.rotate().board)




            #Other team move
            move = None
            while move not in pos.genMoves():
                crdn = input()
                ab = moveSwitch(crdn[0:2])
                cd = moveSwitch(crdn[2:4])
                full = ab+cd
                move = parse(full[0:2]), parse(full[2:4])

            #moke move
            pos = pos.move(move)
            tb, tw, k = searchBoard(pos.board)
            blue.append(move)
            if(len(blue) != 2):
                bluestale.append(blue)
                bluestale = bluestale[1:]
                blue = []
            ov = gameOverCheck(pos, tw, tb, redstale, bluestale, k, False)
            if ov != 0:
                break

            #write new json
            with open('board.json', 'w') as file:
                json.dump({'black': tb, 'white': tw, 'over':ov}, file, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    main()