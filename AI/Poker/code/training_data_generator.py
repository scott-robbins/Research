import numpy as np
import Cards
import utils
import time
import sys
import os

tic = time.time()


def training_ascii():
    date, hours = utils.create_timestamp()
    print '\033[1m\033[32m================================================================\033[0m'
    print 'GENERATING POKER_HAND TRAINING DATA %s - %s' % (date, hours)
    print '[-' + '-' * int(60 * (round + 1) / N) + '-]'
    print '\033[1m[%ss Elapsed] \t \t %s percent complete' % (str(time.time() - tic), str(100 * float(round) / N))
    print '\033[1m\033[32m================================================================\033[0m'


if '-run' in sys.argv:
    hands = []
    deck = Cards.Deck()
    content = ''
    for hand in range(100):
        try:                       # TODO: need to double check for card collisions (or fix root cause)
            table = deck.deal(7)
            content += Cards.show_cards(table) + '\n'
            hands.append(table)
        except IndexError:
            deck.initialize()
            table = deck.deal(7)
            content += Cards.show_cards(table) + '\n'
            hands.append(table)
    print 'Finished Simulating %d Hands. [%ss Elapsed]' % (len(hands), str(time.time()-tic))
    if os.path.isfile('unlabeled_training_data.txt'):
        open('unlabeled_training_data.txt', 'a').write(content)
    else:
        open('unlabeled_training_data.txt', 'w').write(content)


if '-train' in sys.argv:
    if len(sys.argv) >= 3:
        N = int(sys.argv[2])
    else:
        N = 100
    for round in range(N):
        os.system('clear')
        training_ascii()
        os.system('python training_data_generator.py -run')

