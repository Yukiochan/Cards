'''Card.py - Contains classes for cards. Currently, the only class
of cards modeled is Playing Cards'''

from sys import path
path.append('/Users/gregorysun/Documents/python')

import Cards.Shuffle as sh

# Spades, Diamonds, Clubs, Hearts
suits = ['S','D','C','H']


class PlayingCard:
    '''Playing Card class
    contains:
    State:
    value - an int between 1 and 13
    suit - a char in the suits list
    value_str - the value converted
    into a string

    Methods:
    init(value,suit) - takes an integer
    between 1 and 13, value, and either
    a number between 0 and 4 or a character
    in suits, and constructs a playing card.
    The value becomes value, and the suit
    becomes the suit argument if the argument
    is a character. If the suit argument is
    an integer, suit is set to suits[i]
    str() - returns the string representation
    of the card, which is of the form '|vs|'
    where v is the value and s is the suit'''
    def __init__(self,value,suit):
        assert 1 <= value <= 13
        assert suit in suits or suit in range(0,4)
        self.value = value
        if value in range(2,10):
            self.value_str = str(value)
        elif value == 1:
            self.value_str = 'A'
        elif value == 10:
            self.value_str = 'T'
        elif value == 11:
            self.value_str = 'J'
        elif value == 12:
            self.value_str = 'Q'
        else:
            self.value_str = 'K'
        if suit in suits:
            self.suit = suit
        else:
            self.suit = suits[suit]

    def __str__(self):
        return '|' + self.value_str + self.suit + '|'

# Standard 52 card playing deck
StandardDeck = [PlayingCard(value,suit) for suit in suits for value in range(1,14)]