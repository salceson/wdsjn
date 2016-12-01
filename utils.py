# coding: utf-8
from collections import defaultdict

__author__ = "Michał Ciołczyk"

_OGONKI = {
    'ą': 'a',
    'ć': 'c',
    'ę': 'e',
    'ł': 'l',
    'ń': 'n',
    'ó': 'o',
    'ś': 's',
    'ź': 'z',
    'ż': 'z'
}


def dd_int():
    return defaultdict(int)


def dd_float():
    return defaultdict(float)


def deogonkify(txt):
    for ogonek, replacement in _OGONKI.items():
        txt = txt.replace(ogonek, replacement)
    return txt
