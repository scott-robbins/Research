import matplotlib.pyplot as plt
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
        labels = self.classify_raw_data(raw_data)
        if DEBUG:
            print '%d Hands Parsed [%ss Elapsed]' % (len(raw_data), str(time.time()-tic))
        # Label the raw training data
       # self.label_raw_data(labels, raw_data)
        print '%d Hands Labeled [%ss Elapsed]' % (len(raw_data), str(time.time()-tic))

    @staticmethod
    def load_training_data():
        raw_data_in = []
        for table_data in utils.swap('unlabeled_training_data.txt', False):
            raw_data_in.append(table_data)
        print '[*] %d lines of unlabeled training data loaded [%ss Elapsed]' % \
              (len(raw_data_in), str(time.time() - tic))
        return raw_data_in

    def classify_raw_data(self, raw_data):
        classifications = {'High Card': 0, 'Pair': 0, 'Two Pair': 0, 'Three Kind': 0,
                           'Straight': 0, 'Flush': 0, 'Full House': 0, 'Four Kind': 0,
                           'Straight Flush': 0}
        labels = []
        rankings = {0:'High Card', 1: 'Pair', 2: 'Two Pair', 3: 'Three Kind', 4: 'Straight',
                    5: 'Flush', 6: 'Full House', 7: 'Four Kind', 8: 'Straight Flush'}

        mapping = {}
        for k in classifications.keys():
            mapping[k] = 0
        tid = 0    # Table ID for looking back at instances of training set
        pp = 0
        N = 7    # Including 2 Cards in Pocket, each table has 7 Cards
        for table in raw_data:
            '''         '''
            paired = []
            flushed = {68: 0, 72: 0, 67: 0, 83: 0}
            rank = 0
            hand = self.create_cards(table)

            '''           CHECK RANK RELATIONSHIPS          '''
            if hand[0].Rank == hand[1].Rank and (hand[0].Suit != hand[1].Suit):
                paired.append(hand[0].Rank)
                rank = 1
            if hand[0].Rank == (hand[2].Rank or hand[3].Rank or hand[4].Rank or hand[5].Rank or hand[6].Rank):
                paired.append(hand[0].Rank)
                rank = 1
            if hand[1].Rank == (hand[2].Rank or hand[3].Rank or hand[4].Rank or hand[5].Rank or hand[6].Rank):
                paired.append(hand[1].Rank)
                rank = 1
            if hand[2].Rank == (hand[3].Rank or hand[4].Rank or hand[5].Rank or hand[6].Rank):
                paired.append(hand[2].Rank)
                rank = 1
            if hand[3].Rank == (hand[4].Rank or hand[5].Rank or hand[6].Rank):
                paired.append(hand[3].Rank)
                rank = 1
            if hand[4].Rank == (hand[5].Rank or hand[6].Rank):
                paired.append(hand[4].Rank)
                rank = 1



            '''           CHECK SUIT RELATIONSHIPS          '''
            if hand[0].Suit != '' and hand[0].Suit == hand[1].Suit:
                flushed[ord(hand[0].Suit)] += 1
            if hand[0].Suit != '' and hand[0].Suit == (hand[2].Suit or hand[3].Suit or hand[4].Suit or hand[5].Suit or hand[6].Suit):
                flushed[ord(hand[0].Suit)] += 1
            if hand[1].Suit != '' and hand[1].Suit == (hand[2].Suit or hand[3].Suit or hand[4].Suit or hand[5].Suit or hand[6].Suit):
                flushed[ord(hand[1].Suit)] += 1
            if hand[2].Suit != '' and hand[2].Suit == (hand[3].Suit or hand[4].Suit or hand[5].Suit or hand[6].Suit):
                flushed[ord(hand[2].Suit)] += 1
            if hand[3].Suit != '' and hand[3].Suit == (hand[4].Suit or hand[5].Suit or hand[6].Suit):
                flushed[ord(hand[3].Suit)] += 1
            if hand[4].Suit != '' and hand[4].Suit == (hand[5].Suit or hand[6].Suit):
                flushed[ord(hand[4].Suit)] += 1

            '''         Choose the Best hand Made           '''
            if hand[5].Rank == hand[6].Rank:                                # Pair
                paired.append([hand[5].Rank])
            if len(np.unique(np.array(paired))) == 2:                       # Two Pair
                rank = 2
            # if len(straight) >= 5:                                          # Straight
            #     rank = 4
            if len(np.unique(np.array(paired))) == 1 and len(paired) == 3:  # Three Kind
                rank = 3
            for suit in flushed.keys():
                if flushed[suit] >= 4:
                    rank = 5
            if len(np.unique(np.array(paired))) == 2 and len(paired) > 3:   # Full House
                rank = 6
            if rank == 3 and len(paired) == 4:                              # Four Kind
                rank = 7

            self.hand_count[rankings[rank]].append(hand)
            tid += 1
        print '\033[1m==================================================\033[0m'
        bars = []                       # TODO: FOR DEBUGGING PURPOSES SHOW DISTRIBUTION
        for c in self.hand_count.keys():
            bars.append(len(self.hand_count[c]))
            print '%d %s [%f percent]' %\
                  (len(self.hand_count[c]), c, 100*float(len(self.hand_count[c]))/len(raw_data))

        # TODO: For Debugging print examples of hands classified for validation
        ex_pair = self.hand_count['Pair'].pop()
        ex_twopair = self.hand_count['Two Pair'].pop()
        ex_threekind = self.hand_count['Three Kind'].pop()
        #
        return classifications

    def label_raw_data(self, labels, raw):
        content = ''
        ii = 0
        for hand in raw:
            content += hand+'\t'+labels.pop(ii)+'\n'
            ii += 1
        open('training_data.txt', 'w').write(content)

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