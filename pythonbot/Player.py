import argparse
import socket
import sys

#from deuces.deuces import Card, Evaluator
from StartingHand import *
from PercentWin import *
from myCard import * 
from BetCalc import *
from DataParser import *


"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.
"""
class Player:
    def run(self, input_socket):
        f_in = input_socket.makefile()

        # amount bet after flop / 200 - percentage of hand/board
        # cut off for accepting my bets: my bets/200  - percentage of hand/board
        # preflop bet /200 - percentage of starting hand

        # global variables
        d = DataParser()
        minOppPercent = 100 # minimum percept opp goes all in on 
        bc = BetCalc()

        # QUIT WHILE YOU'RE AHEAD FUNCTION ! **************
        
        while True:
            data = f_in.readline().strip()
            if not data:
                print "Gameover, engine disconnected."
                break
            print data

            d.parse(data)

            word = d.word

            if word == "NEWGAME":
                pass
            elif word == "NEWHAND":
                pass
            elif word == "GETACTION":
                actionType = d.actionType
                handRank = d.handRank
                if actionType == "CHECK BET/RAISE":
                    if d.handRank >= 90:
                        bet = bc.getBetAmount("LARGE",d.maxBet,d.minBet)
                        s.send(d.betOrRaise+":"+str(bet)+"\n")
                    elif d.handRank >= 80:
                        bet = bc.getBetAmount("MED",d.maxBet,d.minBet)
                        s.send(d.betOrRaise+":"+str(bet)+"\n")
                    elif d.handRank >= 70:
                        bet = bc.getBetAmount("SMALL",d.maxBet,d.minBet)
                        s.send(d.betOrRaise+":"+str(bet)+"\n")
                    else:
                        s.send(d.betOrRaise+":"+str(d.minBet)+"\n") 

                elif actionType == "CHECK DISCARD DISCARD":
                    s.send(d.shouldDiscard)

                elif actionType == "FOLD CALL":
                    if d.handRank >= 95.0:
                        print "calling to all-in"
                        s.send("CALL\n")
                    else:
                        print "folding to all-in"
                        s.send("FOLD\n")

                elif actionType == "FOLD CALL RAISE":
                    if d.handRank >= 90.0:
                        print "raising"
                        s.send("RAISE:"+str(d.maxRaise/2.0+d.minRaise/2.0)+"\n") 
                    elif d.handRank >= 75.0:
                        print "calling"
                        s.send("CALL\n")
                    else:
                        if d.oppBet <= d.handRank*1.5:
                            print "calling based on bet size"
                            s.send("CALL\n")
                        else:
                            print "folding"
                            s.send("FOLD\n")

                    # 95 for ALL IN CALLS i feel 
                    # also, dont raise a raise unless hand is REAL good >97
                    # no big bets on third round tho


            elif word == "HANDOVER":
                pass
               # if d.cardsShown and d.winner == d.oppName:
                    # differnt amounts of overall bets
                    # near / all-in
                #    if d.winnersPot >= 2.0 * d.stackSize - 5.0:
                 #       oppPercent = d.pw.getWinPercentage()
                  #      minOppPercent = min(oppPercent,minOppPercent)



            elif word == "REQUESTKEYVALUES":
                s.send("FINISH\n")
        s.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Pokerbot.', add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost', help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int, help='Port on host to connect to')
    args = parser.parse_args()

    # Create a socket connection to the engine.
    print 'Connecting to %s:%d' % (args.host, args.port)
    try:
        s = socket.create_connection((args.host, args.port))
    except socket.error as e:
        print 'Error connecting! Aborting'
        exit()

    bot = Player()
    bot.run(s)
