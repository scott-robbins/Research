import numpy as np


class Card:
    Rank = ''
    Suit = ''
    Rankings = {2:'2', 3:'3', 4: '4', 5: '5',
                6:'6', 7:'7', 8: '8', 9: '9',
                10: '10',11: 'J', 12: 'Q', 13: 'J', 14: 'K'}
    Ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    Suits = ['H', 'D', 'C', 'S']

    def __init__(self, R, S):
        if R in self.Ranks and S in self.Suits:
            self.Rank = self.Rankings[R]
            self.Suit = S
        elif R in self.Rankings.values() and S in self.Suits:
            for rank in self.Rankings.keys():
                srank = self.rankings[rank]
                if srank == R:
                    self.Rank = srank
                self.Suit = S
    def show(self):
        card = self.Rank + self.Suit
        print(card)

    def get(self):
        return self.Rank + self.Suit


class Deck:
    cards = []
    dealt = {}

    def __init__(self):
        self.initialize()

    def initialize(self):
        for rs in Card.Ranks:
            for ss in Card.Suits:
                c = Card(rs, ss)
                self.cards.append(c)
                self.dealt[c] = False
        np.random.shuffle(self.cards)

    def deal(self, n_cards):
        cs = []
        for i in range(n_cards):
            c = self.cards.pop()
            cs.append(c)
            self.dealt[c] = True
        return cs


def show_cards(cards):
    hand = ''
    for card in cards:
        hand += card.get()+' '
    return hand


def build_table(p,f,t,r):
    table = []
    for pc in p:
        table.append(pc)
    for fc in f:
        table.append(fc)
    table.append(t.pop())
    table.append(r.pop())
    return table
