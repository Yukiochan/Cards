'''Game.py - a demonstration of the Cards package by implementing
a console solitare game'''

#from sys import path
#path.append('/Users/gregorysun/Documents/python')

from Cards.Shuffle import realistic_shuffle
from Cards.Card import PlayingCard, StandardDeck
from Cards.Dealer import Dealer

def top(lst):
    '''simply returns the top (last elemnt) of a list of -1 if the
    list is empty'''
    if len(lst) > 0:
        return lst[-1]
    else:
        return -1

black = ['S','C']
red = ['D','H']

class Game:
    '''The game class, which is used to keep track of the solitare game
    State:
    dealer - a dealer, which keeps track of the deck
    hidden - a list representing the hidden cards
    stacks - a list representing the cards already
    in play
    spades, diamonds, clubs, hearts - lists represnting the so far completed
    spades, diamonds, clubs, hearts piles
    targets - a list of the suit stacks above to allow for use of for loop
    deck - this is the portion of the deck that can be cycled through by the
    player. Not to be confused with the dealer's deck, which should be empty
    during play.
    dealt - these are the cards the player cycles through that are dealt
    so far (note, this is different from the dealer's dealt)
    lookup - a dictionary mapping input characters to the appropriate stack

    Methods:
    setup() - helper method. Assumes dealer's deck is already shuffles and
    sets up the game of solitare
    init() - initializes a dealer, lookup table shuffles the cards, and then sets up
    reset() - returns all cards back to the deck and shuffles, and then
    sets up
    deal() - puts the to card in deck into dealt and returns the card
    next_three() - deals the next three cards. If there are fewer than 3 cards,
    all remaining cards will be dealt. If the deck is depleted, the dealt cards
    are collected back into the deck and the process repeats.
    peak() - returns a list of the top three dealt cards
    print_game - prints the game in the following format
    deck_size dealt_card1 dealt_card2 dealt_card3       topSpade topDiamond topClub topHeart

        hiddensize1 hiddensize2 hiddensize3 hiddensize4 hiddensize5 hiddensize6 hiddensize7
             stack1      stack2      stack3      stack4      stack5      stack6      stack7
                  1           2           3           4           5           6           7
    The numbers at the bottom are there to make it easier to count the stack numbers
    return_stack(entry) - takes a string, entry, and returns the corresponding stack.
    A wrapper around using the lookup table
    legal_move(stack1,stack2,depth) - checks if moving depth # of cards from stack 2 and
    added to stack2 is a legal rule as dictated by the rules of solitare
    update() - flip over the relevant hidden cards when necessary
    turn(stack1,stack2,depth) - checks if moving depth cards from stack1 to stack2 is
    legal. If it isn't prints "Not a legal move" and does nothing. Otherwise, performs
    the move'''

    def setup(self):
        # create empty lists to hold all of the data
        self.hidden = []
        self.stacks = []
        self.spades = []
        self.diamonds = []
        self.clubs = []
        self.hearts = []
        self.targets = [self.spades,self.diamonds,self.clubs,self.hearts]
        self.deck = []
        self.dealt = []

        # deal each column per the rules of solitare
        for column in range(0,7):
            # initialize lists 
            self.hidden.append([])
            self.stacks.append([])
            # there are precicely column number of hidden cards in
            # each column
            for _ in range(0,column):
                self.hidden[column].append(self.dealer.deal())
            self.stacks[column].append(self.dealer.deal())
        while self.dealer.deck:
            self.deck.append(self.dealer.deal())    
        self.next_three()

    def __init__(self):
        self.dealer = Dealer(StandardDeck)
        self.dealer.full_shuffle()
        self.setup()
        self.lookup = {'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,\
            '7':6,'S':self.spades,'D':self.diamonds,'C':self.clubs\
            ,'H':self.hearts,'d':self.dealt}

    def reset(self):
        self.dealer.reset()
        self.setup()

    def deal(self):
        tmp = self.deck.pop(0)
        self.dealt.append(tmp)
        return tmp

    def next_three(self):
        num_to_deal = min(3,len(self.deck))
        if num_to_deal == 0:
            self.deck = self.dealt[:]
            del self.dealt[:]
            num_to_deal = 3
        for _ in range(0,num_to_deal):
            self.deal()

    def peak(self):
        result = []
        num_to_peak = min(3,len(self.dealt))
        for i in range(num_to_peak,3):
            result.append('|  |')
        for i in range(-num_to_peak,0):
            result.append(str(self.dealt[i]))
        return result

    def print_game(self):
        format1 = "{:<4}{}{}{}    {}{}{}{}"
        format2 = "    {:>4}{:>4}{:>4}{:>4}{:>4}{:>4}{:>4}"
        targets = []
        for stack in self.targets:
            tmp = top(stack)
            if tmp == -1:
                tmp = '|  |'
            else:
                tmp = str(tmp)
            targets.append(tmp)


        peak = self.peak()
        top_row = format1.format(len(self.deck),peak[0],peak[1],peak[2],targets[0],\
            targets[1],targets[2],targets[3])
        print(top_row)
        print()

        hidden = []
        for stack in self.hidden:
            hidden.append(len(stack))
        hidden_row = format2.format(hidden[0],hidden[1],hidden[2],hidden[3],hidden[4]\
            ,hidden[5],hidden[6])
        print(hidden_row)
        max_length = max([len(stack) for stack in self.stacks])
        for i in range(0,max_length):
            row = []
            for stack in self.stacks:
                if len(stack) > i:
                    row.append(str(stack[i]))
                else:
                    row.append('    ')
            row = format2.format(row[0],row[1],row[2],row[3],row[4],row[5]\
                ,row[6])
            print(row)
        print(format2.format(1,2,3,4,5,6,7))

    def return_stack(self,entry):
        if entry.isdigit():
            return self.stacks[self.lookup[entry]]
        else:
            return self.lookup[entry]

    # is it legal to move from stack1 to stack2?
    def legal_move(self,stack1,stack2,depth):
        if depth > len(stack1):
            # if stack not deep enough to remove depth cards
            return False
        elif stack2 == self.dealt:
            # Cannot move cards to the dealt pile
            return False
        else:
            if stack1 == self.dealt and depth != 1:
                # Can only take 1 card from the dealt pile
                return False
            card1 = stack1[-depth]
            card2 = top(stack2)
            if card2 == -1:
                card2_value = 0
            else:
                card2_value = card2.value
            if stack2 in self.stacks:
                if card2_value == 0:
                    # Stack empty, only king can go here
                    return card1.value == 13
                elif card1.value != card2.value - 1:
                    # Card must be equal to one minus the
                    # value of the previous card
                    return False
                else:
                    # Make sure card colors are alternating
                    if card2.suit in red:
                        return card1.suit in black
                    else:
                        return card1.suit in red
            elif card1.value != card2_value + 1:
                # Card added to completed pile must be equal
                # to one plus the previous suit
                return False
            else:
                # Make sure the suits line up
                if stack2 is self.spades:
                    if card1.suit == 'S':
                        return True
                    else:
                        return False
                elif stack2 is self.diamonds:
                    if card1.suit == 'D':
                        return True
                    else:
                        return False
                elif stack2 is self.clubs:
                    if card1.suit == 'C':
                        return True
                    else:
                        return False
                elif stack2 is self.hearts:
                    if card1.suit == 'H':
                        return True
                    else:
                        return False

    def update(self):
        for rank,stack in enumerate(self.stacks):
            if len(stack) == 0 and len(self.hidden[rank]) > 0:
                stack.append(self.hidden[rank].pop())

    def turn(self,str1,str2,depth):
        stack1,stack2 = self.return_stack(str1), self.return_stack(str2)
        if self.legal_move(stack1,stack2,depth):
            tmp = stack1[-depth:]
            for i in range(0,depth):
                stack1.pop(-1)
                stack2.append(tmp[i])
            self.update()
        else:
            print("Not a legal move")



''' The script for running the console game. The game will start by
perfoming the initial deal and printing this deck. Each turn, players
will be prompted with "Enter move: ". They will type in exit or quit,
which quits the game, reset, which resets the game, deal, which deals 3
more cards, or a move in the form stack1 stack2 depth. If the input is
not in one of the above forms, the player will be notified and nothing
will happen. Otherwise, A move is made and then the deck is reprinted'''

game = Game()
while True:
    game.print_game()
    print()
    move = input('Enter move: ')
    if move == "exit" or move == "quit":
        break
    elif move == "deal":
        game.next_three()
    elif move == 'reset':
        game.reset()
    else:
        moves = move.split()
        #print(moves)
        try:
            game.turn(moves[0],moves[1],int(moves[2]))
        except:
            print("Invalid syntax")
