#All game playing code
from Deck import Deck, gamedeck
from Constants import *
import Players
import csv

class Game:
    def __init__(self):
        self.dealer = Players.Dealer()
        self.players = [Players.Learner(self.dealer), Players.CountingLearner(self.dealer)]
    
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
    x = []
    y = []
    for hand in range(NUMHANDS):
        game.dealhand()
        game.playhand()
        #print gamedeck.count
        #print str(float(sum(gamedeck.deck))/float(len(gamedeck.deck)))
        if (len(gamedeck.deck) > (NUMDECKS*52)/2):
            gamedeck.shuffle()
        if (hand%PRINTSTEPS == 0) and (hand != 0):
            x.append([hand, float(game.players[0].numwins)/float(hand)])
            y.append([hand, float(game.players[1].numwins)/float(hand)])
            print "Counting Learner win pct after " + str(hand) + " rounds: " + str(float(game.players[1].numwins)/float(hand))
    with open("stats.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(x)
    with open("stats2.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(y)
    for player in game.players:
        player.printstats()
    with open("output.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(game.players[0].hit)
    with open("midhit.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(game.players[1].midhit)
    with open("highhit.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(game.players[1].highhit)
    with open("lowhit.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(game.players[1].lowhit)