# coding: utf-8
import codecs
import re

__author__ = "Michał Ciołczyk"

_TEXT_SEPARATOR = re.compile('\n#[0-9]{6}\n')


def read_corpora(filename, encoding='utf-8'):
    with codecs.open(filename, encoding=encoding) as f:
        texts = f.read()
        texts = re.split(_TEXT_SEPARATOR, texts)
        return [text.strip().lower() for text in texts]
