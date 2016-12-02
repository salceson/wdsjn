#!/usr/bin/env python
# coding: utf-8
import csv
import pickle
import re
from collections import defaultdict
from math import fsum
from operator import itemgetter

from flection import is_in_dictionary, basic_form
from utils import deogonkify, dd_float

__author__ = "Michał Ciołczyk"

_OMIT_WORDS = [
    'PUSTE',
    'chyba żartujecie że tu jest tyle pytań',
    'wi a',
    'nie chce poddać tej manipulacji i uznać że podsuwacie mi słowa',
    'trolololo'
]
_SPACES_CHECK_REGEX = re.compile('.*\s+.*')
_SPACES_REGEX = re.compile('\s+')
_STIMULUSES = ["alkohol", "wódka", "butelka", "pijak"]
_NUM_OF_ASSOCIATIONS = 20


def _should_omit(word):
    if word in _OMIT_WORDS:
        return True
    if _SPACES_CHECK_REGEX.match(word):
        return False
    else:
        return not is_in_dictionary(word)


def _basic_form_of_phrase(phrase):
    if _SPACES_CHECK_REGEX.match(phrase):
        words = _SPACES_REGEX.split(phrase)
        return ' '.join([basic_form(word) for word in words])
    else:
        return basic_form(phrase)


def _read_computed_associations():
    with open('data/associations.dat', 'rb') as f:
        associations = pickle.loads(f.read())
    for stimulus, values in associations.items():
        denom = fsum(values.values())
        for word, value in values.items():
            associations[stimulus][word] /= denom
    return associations


def _read_real_associations(stimuluses):
    counter = defaultdict(dd_float)
    associations = defaultdict(dd_float)
    stimuluses_files = {stimulus: deogonkify(stimulus) for stimulus in stimuluses}
    for stimulus in stimuluses:
        file_name = stimuluses_files[stimulus]
        with open('data/%s.csv' % file_name) as f:
            reader = csv.reader(f)
            total_count = 0.0
            for row in reader:
                count = float(row[0].strip())
                word = row[1].strip()
                total_count += count
                if _should_omit(word):
                    continue
                counter[stimulus][_basic_form_of_phrase(word.lower())] += count
        for word, count in counter[stimulus].items():
            associations[stimulus][word] = count / total_count
    return associations


def _compare(stimuluses, computed, real, num_of_associations):
    for stimulus in stimuluses:
        computed_for_stimulus = sorted([(k, v) for k, v in computed[stimulus].items()],
                                       key=itemgetter(1), reverse=True)
        real_for_stimulus = sorted([(k, v) for k, v in real[stimulus].items()],
                                   key=itemgetter(1), reverse=True)
        with open('data/comparison_%s.csv' % stimulus, 'w') as f:
            print(stimulus, file=f)
            print('place,real_value,real_word,computed_value,computed_word', file=f)
            for i in range(num_of_associations):
                real_word, real_value = real_for_stimulus[i]
                computed_word, computed_value = computed_for_stimulus[i]
                print('%d,%.4f,%s,%.4f,%s' % (i + 1, real_value, real_word, computed_value, computed_word), file=f)


if __name__ == "__main__":
    real = _read_real_associations(_STIMULUSES)
    computed = _read_computed_associations()
    _compare(_STIMULUSES, computed, real, _NUM_OF_ASSOCIATIONS)
