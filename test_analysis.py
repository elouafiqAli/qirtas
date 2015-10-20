__author__ = 'Ali Elouafiq'

import analysis


def test_reach_ratio():
    assert analysis.reach_ratio([1,1,1,1,1,1,1]) == 1
