import numpy as np
import utils
import Cards
import time
import sys
import os

tic = time.time()
DEBUG = True

class Classifier:

    hand_count = {'High Card': [],
                  'Pair': [],
                  'Two Pair': [],
                  'Three Kind': [],
                  'Straight': [],
                  'Flush': [],
                  'Full House': [],
                  'Four Kind': [],
                  'Straight Flush': []}

    def __init__(self):
        raw_data = self.load_training_data()
        self.label_raw_data(raw_data)
        if DEBUG:
            print '%d Hands Parsed [%ss Elapsed]' % (len(raw_data), str(time.time()-tic))

    @staticmethod
    def load_training_data():
        raw_data_in = []
        for table_data in utils.swap('unlabeled_training_data.txt', False):
            raw_data_in.append(table_data)
        print '[*] %d lines of unlabeled training data loaded [%ss Elapsed]' % \
              (len(raw_data_in), str(time.time() - tic))
        return raw_data_in

    def label_raw_data(self, raw_data):
        classifications = {'High Card': 0,'Pair':0,'Two Pair': 0, 'Three Kind': 0,
                           'Straight': 0, 'Flush': 0, 'Full House': 0, 'Four Kind': 0,
                           'Straight Flush': 0}
        mapping = {}
        for k in classifications.keys():
            mapping[k] = 0
        tid = 0    # Table ID for looking back at instances of training set
        pp = 0
        N = 7    # Including 2 Cards in Pocket, each table has 7 Cards
        for table in raw_data:
            '''         '''
            hand = self.create_cards(table)
            label = ''
            if hand[0].Rank == hand[1].Rank:
                label = 'Pair'
                pp += 1

            flushed = []
            paired = []
            for ci in hand:
                for cj in hand:
                    if (ci.Rank == cj.Rank and ci.Suit != cj.Suit) or (ci.Rank != cj.Rank and ci.Suit == cj.Suit):
                        if ci.Rank == cj.Rank:
                            mapping['Pair'] += 1
                            paired.append(ci.Rank)
                            paired.append(cj.Rank)
                        if ci.Suit == cj.Suit:
                            flushed.append(ci)
                            flushed.append(ci)
            if np.unique(np.array(paired)).shape[0] == 2:
                mapping['Two Pair'] += 1
            if np.unique(np.array(paired)).shape[0] == 3:
                mapping['Three Kind'] += 1
            if np.unique(np.array(paired)).shape[0] == 3 and np.unique(np.array(flushed)).shape[0] == 3:
                mapping['Full House'] += 1
            if len(flushed) >= 5:
                mapping['Flush'] += 1
            if np.unique(np.array(paired)).shape[0] == 1 and len(paired)>=4:
                mapping['Four Kind']
            try:
                classifications[tid] = label
                self.hand_count[classifications[tid]] += 1
            except:
                pass
            tid += 1
        print '%d Pocket Pairs' % pp
        print '%d Pairs' % mapping['Pair']
        print '%d Two Pair(s)' % mapping['Two Pair']
        print '%d Three Kind' % mapping['Three Kind']
        print '%d Flushes' % mapping['Flush']
        print '%d Full Houses(s)' % mapping['Full House']
        print '%d Four Kind(s)' % mapping['Four Kind']

    @staticmethod
    def create_cards(cardstr_arr):
        cards_out = []
        faces = ['J', 'Q', 'K', 'A']
        suits = ['C', 'D', 'S', 'H']
        fmaps = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        for card in cardstr_arr.replace('\n','').split(' '):
            try:
                r = list(card).pop(0)
                s = list(card).pop()
                if r in faces:
                    r = fmaps[r]
                elif card:
                    r = int(r)
                cards_out.append(Cards.Card(r, s))
            except Exception:
                pass
        return cards_out


if __name__ == '__main__':
    labeler = Classifier()

# EOF