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
            flushed = []
            rank = 0
            hand = self.create_cards(table)

            # Check for pocket pair, or pair
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
            if hand[5].Rank == hand[6].Rank:
                paired.append([hand[5].Rank])
            if len(np.unique(np.array(paired))) == 2:
                rank = 2
            if len(np.unique(np.array(paired))) == 3:
                rank = 3
            self.hand_count[rankings[rank]].append(hand)
            tid += 1
        print '\033[1m==================================================\033[0m'
        bars = []                       # TODO: FOR DEBUGGING PURPOSES SHOW DISTRIBUTION
        for c in self.hand_count.keys():
            bars.append(len(self.hand_count[c]))
            print '%d %s [%f percent]' %\
                  (len(self.hand_count[c]), c, 100*float(len(self.hand_count[c]))/len(raw_data))
        ex = self.hand_count['Pair'].pop(np.random.random_integers(0,100,1)[0])
        print Cards.show_cards(ex)

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