#!/usr/bin/env python
# coding: utf-8

import pickle

if __name__ == "__main__":
    with open('data/corpora.dat', 'rb') as f:
        corpora = pickle.loads(f.read())
    with open('data/corpora_unprocessed.dat', 'rb') as f:
        unprocessed = pickle.loads(f.read())
    try:
        while True:
            print('Enter word to search, ctrl+d to end...')
            word = input('Word: ')
            for i, text in enumerate(corpora):
                if word in text:
                    print(' '.join(text))
                    print(''.join(unprocessed[i]))
                    print()
    except KeyboardInterrupt:
        pass
