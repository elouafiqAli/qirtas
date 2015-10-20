from __future__ import division
from math import sqrt, pow

__author__ = 'Ali Elouafiq'


def reach_estimation(unique_comments, users_mentioned, friends, likes, shares, privacy):

    stickiness = sqrt( (unique_comments + users_mentioned) * likes / 7) + sqrt(shares * likes + shares ** 2)

    if unique_comments == 0:
        reach = (likes + users_mentioned) * 16 + shares * 33
    else:
        reach = (likes + users_mentioned) * 8 + (friends - likes) * pow(2, - 33 / stickiness)

    if privacy is not 'EVERYONE' and reach > friends:
        return friends
    else:
        return reach


def reach_ratio(top_elements):

    sigma = 0
    length = len(top_elements)
    for weight in range(length):
        sigma += top_elements[weight]*(length-weight)

    ratio = 2*sigma/(length**2+length)
    return ratio