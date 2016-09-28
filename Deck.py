#Code for the Deck of cards
from random import shuffle
from Constants import NUMDECKS

class Deck:
    def __init__(self, num):
        self.numberofdecks = num
        self.count = 0
        self.truecount = 0
        self.deck = []
        self.shuffle()

        
    def shuffle(self):
        lst = []
        for x in range(self.numberofdecks):
            for y in range(2,10):
                lst += [y]*4
            lst += [10]*16
            lst += [11]*4
        shuffle(lst)
        self.count = 0
        self.deck = lst
    
    def countcard(self, card):
        if card < 7:
            self.count += 1
        if card > 9:
            self.count -= 1
        self.truecount = float(self.count) / (float(len(self.deck))/52.)
        return
    
    def dealcard(self, faceup):
        card = self.deck[0]
        self.deck = self.deck[1:]
        if faceup:
            self.countcard(card)
            #print "Card dealt faceup"
        #else:
            #print "Card dealt facedown"
        return card
    
gamedeck = Deck(NUMDECKS)