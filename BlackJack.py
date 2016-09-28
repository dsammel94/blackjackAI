#All game playing code
from Deck import Deck, gamedeck
from Constants import *
import Players
import csv

class Game:
    def __init__(self):
        self.dealer = Players.Dealer()
        self.players = [Players.Dealer(), Players.Counter(), Players.Learned(self.dealer), Players.CountingLearned(self.dealer), Players.DumbPlayer()]
    
    def dealhand(self):
        #Deal first card
        for player in self.players:
            card = gamedeck.dealcard(FACEDOWN)
            player.receivecard(card)
        card = gamedeck.dealcard(FACEDOWN)
        self.dealer.receivecard(card)
        
        #Deal second card
        for player in self.players:
            card = gamedeck.dealcard(FACEUP)
            player.receivecard(card)
        card = gamedeck.dealcard(FACEUP)
        self.dealer.receivecard(card)
        
    def playhand(self):
        for player in self.players:
            player.play()
        self.dealer.play()
        #assess if any players won, count the cards that were hidden until now
        gamedeck.countcard(self.dealer.hiddencard)
        for player in self.players:
            gamedeck.countcard(player.hiddencard)
            if(player.blackjack and not self.dealer.blackjack):
                player.win()
            elif(self.dealer.blackjack):
                player.lose(True)
            elif player.bust == True:
                player.lose(False)
            elif(self.dealer.bust == True):
                player.win()
            elif(player.hand > self.dealer.hand):
                player.win()
            else:
                player.lose(False)
        #to reset dealer's hand
        self.dealer.lose(False)

if __name__ == "__main__":
    game = Game()
    for hand in range(NUMHANDS):
        game.dealhand()
        game.playhand()
        if (len(gamedeck.deck) > (NUMDECKS*52)/2):
            gamedeck.shuffle()
        if (hand%PRINTSTEPS == 0) and (hand != 0):
            print "Hands complete: " + str(hand)
    for player in game.players:
        player.printstats()
