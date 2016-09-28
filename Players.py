#code for the players
from Deck import gamedeck
from Constants import *
import random
import csv

class Dealer:
    def __init__(self):
        self.hand = 0
        self.hiddencard = None
        self.numwins = 0
        self.bust = False
        self.blackjack = False
    
    def play(self):
        if(self.hand == 21):
            self.blackjack == True
        #hit on less than 16
        while(self.hand <= 16):
            card = gamedeck.dealcard(FACEUP)
            if (card == 11) and ((self.hand + card) > 21):
                card = 1
            self.hand += card
        if self.hand > 21:
            self.bust = True
        return
    
    def receivecard(self, card):
        if self.hand == 0:
            self.hiddencard = card
        self.hand += card
        if self.hand == 22:
            self.card = 12
        
    def win(self):
        self.numwins += 1
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def lose(self,dealerbj):
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def printstats(self):
        print "-------------------------------------------"
        print "Dealer playstyle"
        print ""
        print "Number of wins: " + str(self.numwins)
        print "Win percentage: " + str(float(self.numwins)/float(NUMHANDS))
        print "-------------------------------------------"

class Learner:
    def __init__(self, dealer):
        self.hand = 0
        self.hiddencard = None
        self.dealer = dealer
        self.dealershow = 0
        self.lasthit = None
        self.numwins = 0
        self.bust = False
        self.hit = [[.5]*22 for _ in range(12)]
        self.blackjack = False
        
    def play(self):
        self.dealershow = self.dealer.hand - self.dealer.hiddencard
        if self.hand == 21:
            self.blackjack = True
            return
        #hit on less than 16
        self.lasthit = self.hand
        while(1):
            if random.random() < self.hit[self.dealershow][self.hand]:
                self.lasthit = self.hand
                card = gamedeck.dealcard(FACEUP)
                if (card == 11) and ((self.hand + card) > 21):
                    card = 1
                self.hand += card
            else:
                break
            if self.hand > 21:
                self.bust = True
                break
        return
    
    def receivecard(self, card):
        if self.hand == 0:
            self.hiddencard = card
        self.hand += card
        if self.hand == 22:
            self.hand = 12
    
    def win(self):
        self.numwins += 1
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def lose(self, dealerbj):
        if(not dealerbj):
            if self.bust:
                self.hit[self.dealershow][self.lasthit] = max(self.hit[self.dealershow][self.lasthit] - .01, 0.)
            else:
                self.hit[self.dealershow][self.lasthit] = min(self.hit[self.dealershow][self.lasthit] + .01, 1.)
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def printstats(self):
        print "-------------------------------------------"
        print "Learner playstyle"
        print ""
        print "Number of wins: " + str(self.numwins)
        print "Win percentage: " + str(float(self.numwins)/float(NUMHANDS))
        print "Open output.csv for final matrix"
        print "-------------------------------------------"
        

class CountingLearner:
    def __init__(self, dealer):
        self.hand = 0
        self.hiddencard = None
        self.dealer = dealer
        self.dealershow = 0
        self.lasthit = None
        self.lasthitcount = 0
        self.numwins = 0
        self.bust = False
        self.midhit = [[.5]*22 for _ in range(12)]
        self.highhit = [[.5]*22 for _ in range(12)]
        self.lowhit = [[.5]*22 for _ in range(12)]
        self.blackjack = False
        
    def play(self):
        self.dealershow = self.dealer.hand - self.dealer.hiddencard
        if self.hand == 21:
            self.blackjack = True
            return
        #hit on less than 16
        self.lasthit = self.hand
        self.lasthitcount = gamedeck.truecount
        while(1):
            if gamedeck.truecount > HIGHTHRESH:
                model = self.highhit
            elif gamedeck.truecount < LOWTHRESH:
                model = self.lowhit
            else:
                model = self.midhit
            if random.random() < model[self.dealershow][self.hand]:
                self.lasthit = self.hand
                self.lasthitcount = gamedeck.truecount
                card = gamedeck.dealcard(FACEUP)
                if (card == 11) and ((self.hand + card) > 21):
                    card = 1
                self.hand += card
            else:
                break
            if self.hand > 21:
                self.bust = True
                break
        return
    
    def receivecard(self, card):
        if self.hand == 0:
            self.hiddencard = card
        self.hand += card
        if self.hand == 22:
            self.hand = 12
    
    def win(self):
        self.numwins += 1
        #if not self.blackjack:
        #   self.winsoncount[self.dealershow][self.lasthit] += 1
        #    winpct = float(self.winsoncount[self.dealershow][self.lasthit])/float(self.hitsoncount[self.dealershow][self.lasthit])
        #    self.hit[self.dealershow][self.lasthit] = winpct #.1*self.hit[self.dealershow][self.lasthit] + .9*(winpct)
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def lose(self, dealerbj):
        #winpct = float(self.winsoncount[self.dealershow][self.lasthit])/float(self.hitsoncount[self.dealershow][self.lasthit])
        if(not dealerbj):
            if self.lasthitcount > HIGHTHRESH:
                model = self.highhit
            elif self.lasthitcount < LOWTHRESH:
                model = self.lowhit
            else:
                model = self.midhit
            if self.bust:
                model[self.dealershow][self.lasthit] = max(0.0, model[self.dealershow][self.lasthit] - .01)
            else:
                model[self.dealershow][self.lasthit] = min(1.0, model[self.dealershow][self.lasthit] + .01)
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def printstats(self):
        print "-------------------------------------------"
        print "Learner playstyle with counting"
        print ""
        print "Number of wins: " + str(self.numwins)
        print "Win percentage: " + str(float(self.numwins)/float(NUMHANDS))
        print "Open midhit.csv, highhit.csv, and lowhit.csv for final matrices"
        print "-------------------------------------------"

class Learned:
    def __init__(self, dealer):
        self.hand = 0
        self.hiddencard = None
        self.dealer = dealer
        self.dealershow = 0
        self.numwins = 0
        self.bust = False
        with open('output.csv', 'rb') as inf:
            data = list(csv.reader(inf, skipinitialspace=True))
            #data = [i for i in data if i] ## add to deal w/ blank lines in data file
        self.hit = data
        self.blackjack = False
        
    def play(self):
        self.dealershow = self.dealer.hand - self.dealer.hiddencard
        if self.hand == 21:
            self.blackjack = True
            return
        while(1):
            if random.random() < float(self.hit[self.dealershow][self.hand]):
                card = gamedeck.dealcard(FACEUP)
                if (card == 11) and ((self.hand + card) > 21):
                    card = 1
                self.hand += card
            else:
                break
            if self.hand > 21:
                self.bust = True
                break
        return
    
    def receivecard(self, card):
        if self.hand == 0:
            self.hiddencard = card
        self.hand += card
        if self.hand == 22:
            self.hand = 12
    
    def win(self):
        self.numwins += 1
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def lose(self, dealerbj):
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def printstats(self):
        print "-------------------------------------------"
        print "Learned playstyle"
        print ""
        print "Number of wins: " + str(self.numwins)
        print "Win percentage: " + str(float(self.numwins)/float(NUMHANDS))
        print "-------------------------------------------"
        

class CountingLearned:
    def __init__(self, dealer):
        self.hand = 0
        self.hiddencard = None
        self.dealer = dealer
        self.dealershow = 0
        self.lasthit = None
        self.lasthitcount = 0
        self.numwins = 0
        self.bust = False
        with open('midhit.csv', 'rb') as inf:
            data = list(csv.reader(inf, skipinitialspace=True))
            data = [i for i in data if i]
        self.midhit = data
        with open('highhit.csv', 'rb') as inf:
            data = list(csv.reader(inf, skipinitialspace=True))
            data = [i for i in data if i]
        self.highhit = data
        with open('lowhit.csv', 'rb') as inf:
            data = list(csv.reader(inf, skipinitialspace=True))
            data = [i for i in data if i]
        self.lowhit = data
        self.blackjack = False
        
    def play(self):
        self.dealershow = self.dealer.hand - self.dealer.hiddencard
        if self.hand == 21:
            self.blackjack = True
            return
        #hit on less than 16
        self.lasthit = self.hand
        self.lasthitcount = gamedeck.truecount
        while(1):
            if gamedeck.truecount > HIGHTHRESH:
                model = self.highhit
            elif gamedeck.truecount < LOWTHRESH:
                model = self.lowhit
            else:
                model = self.midhit
            if random.random() < float(model[self.dealershow][self.hand]):
                self.lasthit = self.hand
                self.lasthitcount = gamedeck.truecount
                card = gamedeck.dealcard(FACEUP)
                if (card == 11) and ((self.hand + card) > 21):
                    card = 1
                self.hand += card
            else:
                break
            if self.hand > 21:
                self.bust = True
                break
        return
    
    def receivecard(self, card):
        if self.hand == 0:
            self.hiddencard = card
        self.hand += card
        if self.hand == 22:
            self.hand = 12
    
    def win(self):
        self.numwins += 1
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def lose(self, dealerbj):
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def printstats(self):
        print "-------------------------------------------"
        print "Learned playstyle with counting"
        print ""
        print "Number of wins: " + str(self.numwins)
        print "Win percentage: " + str(float(self.numwins)/float(NUMHANDS))
        print "-------------------------------------------"


class Counter:
    def __init__(self):
        self.hand = 0
        self.hiddencard = None
        self.numwins = 0
        self.numhigh = 0
        self.numlow = 0
        self.winonlow = 0
        self.winonhigh = 0
        self.bust = False
        self.hit = [0]*4 + [1]*18
        self.blackjack = False
    
    def play(self):
        if self.hand == 21:
            self.blackjack = True
        #hit on less than 16
        while(self.hand <= 16):
            card = gamedeck.dealcard(FACEUP)
            if (card == 11) and ((self.hand + card) > 21):
                card = 1
            self.hand += card
        if self.hand > 21:
            self.bust = True
        return

    def receivecard(self, card):
        if self.hand == 0:
            self.hiddencard = card
        self.hand += card

    def win(self):
        self.numwins +=1
        if(gamedeck.truecount > HIGHTHRESH):
            self.numhigh += 1
            self.winonhigh += 1
        elif (gamedeck.truecount < LOWTHRESH):
            self.numlow += 1
            self.winonlow += 1
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def lose(self, dealerbj):
        if(gamedeck.truecount < LOWTHRESH):
            self.numlow += 1
        elif(gamedeck.truecount > HIGHTHRESH):
            self.numhigh += 1
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def printstats(self):
        print "-------------------------------------------"
        print "Card Counting style"
        print ""
        print "Number of wins: " + str(self.numwins)
        print "Win percentage: " + str(float(self.numwins)/float(NUMHANDS))
        print "Wins on high  : " + str(self.winonhigh)
        print "Win on high % : " + str(float(self.winonhigh)/float(self.numhigh))
        print "Wins on low   : " + str(self.winonlow)
        print "Win on low %  : " + str(float(self.winonlow)/float(self.numlow))
        print "-------------------------------------------"
        
class DumbPlayer:
    def __init__(self):
        self.hand = 0
        self.hiddencard = None
        self.numwins = 0
        self.bust = False
        self.blackjack = False
    
    def play(self):
        if self.hand == 21:
            self.blackjack = True
        while(random.random() < .5):
            card = gamedeck.dealcard(FACEUP)
            if (card == 11) and ((self.hand + card) > 21):
                card = 1
            self.hand += card
        if self.hand > 21:
            self.bust = True
        return

    def receivecard(self, card):
        if self.hand == 0:
            self.hiddencard = card
        self.hand += card

    def win(self):
        self.numwins +=1
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def lose(self, dealerbj):
        self.hand = 0
        self.hiddencard = None
        self.bust = False
        self.blackjack = False
    
    def printstats(self):
        print "-------------------------------------------"
        print "Dumb style"
        print ""
        print "Number of wins: " + str(self.numwins)
        print "Win percentage: " + str(float(self.numwins)/float(NUMHANDS))
        print "-------------------------------------------"