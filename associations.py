# coding: utf-8
from collections import defaultdict

from utils import dd_int, dd_float

__author__ = "Michał Ciołczyk"


def _compute_window(idx, window_width, arr):
    left_min = max(idx - window_width, 0)
    left_max = idx
    right_min = idx + 1
    right_max = min(idx + window_width + 1, len(arr))
    return arr[left_min:left_max] + arr[right_min:right_max]


def compute_cooccurrences(corpora, stimuluses, window_width):
    cooccurrences = defaultdict(dd_int)
    for text in corpora:
        for i in range(len(text)):
            for stimulus in stimuluses:
                if text[i] == stimulus:
                    words_to_search = _compute_window(i, window_width, text)
                    for word in words_to_search:
                        if word == stimulus:
                            continue
                        cooccurrences[stimulus][word] += 1
    return cooccurrences


def compute_associations(occurrences, cooccurrences, stimuluses, alpha, beta, gamma):
    associations = defaultdict(dd_float)
    words_num = len(occurrences.keys())
    beta_q = beta * words_num
    gamma_q = gamma * words_num
    for stimulus in stimuluses:
        for word, cooccurrences_num in cooccurrences[stimulus].items():
            if occurrences[word] > beta_q:
                associations[stimulus][word] = cooccurrences_num / (occurrences[word] ** alpha)
            else:
                associations[stimulus][word] = cooccurrences_num / gamma_q
    return associations


if __name__ == "__main__":
    tab = [i for i in range(10)]
    tab_window = _compute_window(0, 2, tab)
    assert tab_window == [1, 2]
    tab_window = _compute_window(1, 2, tab)
    assert tab_window == [0, 2, 3]
    tab_window = _compute_window(2, 2, tab)
    assert tab_window == [0, 1, 3, 4]
    tab_window = _compute_window(3, 2, tab)
    assert tab_window == [1, 2, 4, 5]
    tab_window = _compute_window(8, 2, tab)
    assert tab_window == [6, 7, 9]
    tab_window = _compute_window(9, 2, tab)
    assert tab_window == [7, 8]
