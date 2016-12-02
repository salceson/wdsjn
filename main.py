#!/usr/bin/env python
# coding: utf-8
import pickle
from operator import itemgetter

from associations import compute_associations, compute_cooccurrences
from pap import read_corpora
from preprocess import preprocess_corpora

__author__ = "Michał Ciołczyk"

# Algorithm parameters:
_WINDOW_WIDTH = 12
_ALPHA = 0.66
_BETA = 0.00002
_GAMMA = 0.00002
_MIN_OCCURRENCES_NUM = 10
# Stimuluses to compute associations for:
_STIMULUSES = ["alkohol", "wódka", "butelka", "pijak"]
# Corpora file:
_CORPORA_FILENAME = "data/pap.txt"
_CORPORA_ENCODING = "utf-8"
# Should read data from file instead of computing?
_READ_FROM_FILES = False

if __name__ == "__main__":
    if not _READ_FROM_FILES:
        print("Reading corpora...")
        corpora = read_corpora(_CORPORA_FILENAME, _CORPORA_ENCODING)
        print("Done")
        print("Preprocessing corpora...")
        corpora, occurrences = preprocess_corpora(corpora, _MIN_OCCURRENCES_NUM, _STIMULUSES)
        print("Done")
        print("Saving preprocessed corpora...")
        with open('data/corpora.dat', 'wb') as f:
            f.write(pickle.dumps(corpora))
        with open('data/occurrences.dat', 'wb') as f:
            f.write(pickle.dumps(occurrences))
        print("Done")
        print("Computing cooccurrences for window width: %d" % _WINDOW_WIDTH)
        cooccurrences = compute_cooccurrences(corpora, _STIMULUSES, _WINDOW_WIDTH)
        print("Done")
        print("Saving cooccurrences...")
        with open('data/cooccurrences.dat', 'wb') as f:
            f.write(pickle.dumps(cooccurrences))
        print("Done")
        print("Computing associations...")
        associations = compute_associations(occurrences, cooccurrences, _STIMULUSES, _ALPHA, _BETA, _GAMMA)
        print("Done")
        print("Saving associations...")
        with open('data/associations.dat', 'wb') as f:
            f.write(pickle.dumps(associations))
        print("Done")
    else:
        # Read from pickle saved data
        print("Reading associations...")
        with open('data/associations.dat', 'rb') as f:
            associations = pickle.loads(f.read())
        print("Done")
    for stimulus, stimulus_associations in associations.items():
        print("Associations for %s:" % stimulus)
        associations_sorted = sorted([(word, strength) for word, strength in stimulus_associations.items()],
                                     key=itemgetter(1), reverse=True)
        for word, strength in associations_sorted:
            print("\t%s %.6f" % (word, strength))
