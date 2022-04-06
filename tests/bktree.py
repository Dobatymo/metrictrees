from __future__ import generator_stop

from unittest import SkipTest, TestCase

from metrictrees.bktree import BKTree


class BKTreeTest(TestCase):
    def test_range(self):
        value = range(10)

        tree = BKTree(lambda a, b: abs(b - a))
        tree.update(value)
        truth = list(value)

        self.assertEqual(list(tree), truth)

    def test_words(self):
        try:
            from nltk import download
            from nltk.corpus import words
            from polyleven import levenshtein
        except ImportError:
            raise SkipTest("Missing imports. pip install nltk polyleven")

        download("words")

        maxdistance = 2
        words = words.words()

        def find_closest(word, results):
            return sorted((levenshtein(word, w), w) for w in words)[:results]

        tree = BKTree(levenshtein)
        tree.update(words)

        for word in ("asdqwe", "abbaration", "illegitimate", "penourius"):

            results = sorted(tree.find(word, maxdistance))  # bktree
            truth = find_closest(word, len(results))  # linear search

            self.assertEqual(results, truth)
