import itertools
import wordutil
import random
import time
import sys
import os


alphas = ['a','b','c','d','e','f','g','h','i','j','k','l',
          'm','n','o','p','q','r','s','t','u','v','w','x',
          'y','z', 'A','B','C','D','E','F','G','H','I','J',
          'K','L','M','N','O','P','Q','R','S','T','U','V',
          'W','X','Y','Z']

symbol = ['0','1','2','3','4','5','6','7','8','9','-','=',
          '!','@','#','$','%','^','&','*','(',')','_','+',
          '[',']','\\', ';', "'", ',', '.','<','>',':','"',
          '{','}','|']

real_words = wordutil.swap('words.txt', False)


def test_gen(n_letters, n_words):
    tic = time.time()
    words_out = []
    tics = 0
    while len(words_out) < n_words:
        test_word = wordutil.arr2str(random.sample(alphas, n_letters)).replace(' ', '')
        if test_word in real_words:
            words_out.append(test_word)
        tics += 1
        if tics % 1250 == 0:
            print ' - [%d Iterations Completed\t%d Words Created]' % (tics, len(words_out))
    print '[*] Finished Generating %d words [%s Elapsed]' % (n_words, str(time.time()-tic))
    return words_out


guess = test_gen(4, 5)
print guess
