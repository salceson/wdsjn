# coding: utf-8
from collections import defaultdict

from utils import dd_int, dd_float

__author__ = "Michał Ciołczyk"


def compute_cooccurrences(corpora, stimuluses, window_width):
    cooccurrences = defaultdict(dd_int)
    for text in corpora:
        for i in range(len(text)):
            for stimulus in stimuluses:
                if text[i] == stimulus:
                    left_min = max(i - window_width, 0)
                    left_max = i
                    right_min = i + 1
                    right_max = min(i + window_width + 1, len(text))
                    words_to_search = text[left_min:left_max] + text[right_min:right_max]
                    for word in words_to_search:
                        cooccurrences[stimulus][word] += 1
    return cooccurrences


def compute_associations(corpora, occurrences, cooccurrences, stimuluses, alpha, beta, gamma):
    associations = defaultdict(dd_float)
    words_num = sum([len(text) for text in corpora])
    beta_q = beta * words_num
    gamma_q = gamma * words_num
    for stimulus in stimuluses:
        for word, cooccurrences_num in cooccurrences[stimulus].items():
            if occurrences[word] > beta_q:
                associations[stimulus][word] = cooccurrences_num / (occurrences[word] ** alpha)
            else:
                associations[stimulus][word] = cooccurrences_num / gamma_q
    return associations
