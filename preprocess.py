# coding: utf-8
import re
from collections import defaultdict

from flection import basic_form

_NOT_LETTERS = re.compile('[^a-ząćęłóńśżź]+')
_SPACES = re.compile('\s+')


def preprocess_corpora(corpora, min_occurrences_num, stimuluses):
    corpora = [_NOT_LETTERS.sub(' ', text) for text in corpora]
    corpora = [[basic_form(word) for word in _SPACES.split(text.lower()) if len(word) > 0] for text in corpora]
    occurrences = defaultdict(int)
    for text in corpora:
        for word in text:
            occurrences[word] += 1
    corpora = [[word for word in text if occurrences[word] > min_occurrences_num or word in stimuluses]
               for text in corpora]
    for word, occurrences_num in occurrences.items():
        if occurrences_num <= min_occurrences_num:
            occurrences.pop(word, None)
    return corpora, occurrences
