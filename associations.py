# coding: utf-8
from collections import defaultdict


def compute_cooccurrences(corpora, stimuluses, window_width):
    cooccurrences = defaultdict(lambda: defaultdict(int))
    for stimulus in stimuluses:
        for text in corpora:
            for i in range(len(text)):
                min_idx = max(i - window_width, 0)
                max_idx = min(i + window_width, len(text) - 1)
                words_to_search = text[min_idx:max_idx]
                for word in words_to_search:
                    cooccurrences[stimulus][word] += 1
    return cooccurrences


def compute_associations(corpora, occurrences, cooccurrences, stimuluses, alpha, beta, gamma):
    associations = defaultdict(lambda: defaultdict(float))
    Q = sum([len(text) for text in corpora])
    for stimulus in stimuluses:
        for word, cooccurrences_num in cooccurrences[stimulus].items():
            if occurrences[word] > beta * Q:
                associations[stimulus][word] = cooccurrences_num / (occurrences[word] ** alpha)
            else:
                associations[stimulus][word] = cooccurrences_num / (gamma * occurrences[word])
    return associations
