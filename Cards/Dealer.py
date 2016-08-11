'''Dealer.py - implements the dealer class'''


#from sys import path
#path.append('/Users/gregorysun/Documents/python')

from Cards.Shuffle import realistic_shuffle
from Cards.Card import StandardDeck, PlayingCard

class Dealer:
    '''A dealer that can be used for implementing card games
    State:
    deck - a list representation of the current deck
    dealt - a list of all of the cards dealt

    Methods:
    init(deck) - takes a list, deck and initializes the 
    dealer's deck to deck, and the dealt list to empty
    deal() - pops the top card (defined as the first
    element of the deck) out and appends it to the list
    of dealt cards. Also returns the dealt card
    recombine() - put the dealt cards back into the
    remaining deck
    full_shuffle() - a wrapper for full_shuffle on the
    deck
    print_deck() - prints each of the cards in the deck
    in order from top to bottom
    reset() - A wrapper around the common sequence
    recombine, reset'''
    def __init__(self, deck):
        assert isinstance(deck, list)
        self.deck = deck
        self.dealt = []

    def deal(self):
        tmp = self.deck.pop(0)
        self.dealt.append(tmp)
        return tmp

    def recombine(self):
        self.deck += self.dealt
        self.dealt = []

    def full_shuffle(self):
        self.deck = realistic_shuffle(self.deck)

    def print_deck(self):
        result = ""
        for card in self.deck:
            result += str(card)
        print(result)

    def reset(self):
        self.recombine()
        self.full_shuffle()


'''d = Dealer(StandardDeck)
d.full_shuffle()
for _ in range(0,10):
    d.deal()
d.print_deck()
d.reset()
d.print_deck()'''
