#!/usr/bin/env python

"""Class to play the game of nim
   https://en.wikipedia.org/wiki/Nim
"""
from random import randrange

class Nim:
    def __init__(self, piles, misery=True):
        """Misery means you want to avoid taking the last object."""
        self.piles = list(piles)
        self.misery = misery
        self.fpom = True # first player is on-move

    def play_move(self, index, count):
        """Remove count objects from pile at index.
           Return value of true means the game is over"""
        self.piles[index] -= count
        if self.piles[index] == 0:
            del self.piles[index]
        self.fpom = not self.fpom
        if len(self.piles) == 0:
            return True

    def get_move(self):
        """Get a move to play. If there is a winning move, play it. Otherwise remove 1 element from a pile.
           Move is specified by index, count"""
        ones = sum([1 if pile == 1 else 0 for pile in self.piles])
        if ones == len(self.piles): # no choice
            return (randrange(0, len(self.piles)), 1)
        multis = sum([1 if pile > 1 else 0 for pile in piles])
        if multis > 1: # misery and normal play is the same
            nim_sum = self.piles[0]
            for index in range(1, len(self.piles)):
                nim_sum ^= self.piles[index]
            if nim_sum == 0: # player on move is fucked
                return (randrange(0, len(self.piles)), 1)
            for index in range(len(self.piles)):
                if self.piles[index] ^ nim_sum < self.piles[index]:
                    break
            new_sum = self.piles[index] ^ nim_sum # reduce pile to this amount
            return (index, self.piles[index] - new_sum)

        # There's only one pile left with more than one element.
        # in the misery version, leave an odd number of total) piles
        # in the normal version leave an even number
        for index in range(len(self.piles)):
            if self.piles[index] > 1:
                break
        if len(self.piles) & 1 == 0: # odd
            if self.misery:
                return (index, self.piles[index] - 1)
            else:
                return (index, self.piles[index])
        else:
            if self.misery:
                return (index, self.piles[index])
            else:
                return (index, self.piles[index] - 1)

if __name__ == '__main__':
    done = False
    piles = [999,999, 4]
    nim = Nim(piles)
    while(not done):
        if nim.fpom:
            player = "player 1"
        else:
            player = "player 2"
        amove = nim.get_move()
        done = nim.play_move(amove[0], amove[1])
        print(player, "plays", amove, "piles are now", nim.piles)
    fpw = bool(nim.misery ^ nim.fpom)
    if fpw:
        print("player 1 wins")
    else:
        print("player 2 wins")
