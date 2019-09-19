import numpy as np
import Cards
import utils
import time
import sys
import os

tic = time.time()


if '-run' in sys.argv:
    hands = []
    deck = Cards.Deck()
    content = ''
    for hand in range(1000):
        try:
            pocket = deck.deal(2)
            flop = deck.deal(3)
            turn = deck.deal(1)
            rivr = deck.deal(1)
            table = Cards.build_table(pocket, flop, turn, rivr)
            content += Cards.show_cards(table) + '\n'
            hands.append(table)
            if len(deck.dealt.values()) >= 42:
                deck.initialize()
        except IndexError:
            print len(deck.dealt.values())
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
        os.system('python training_data_generator.py -run')

