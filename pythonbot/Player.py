import argparse
import socket
import sys

#from deuces.deuces import Card, Evaluator
from StartingHand import *
from PercentWin import *
from myCard import * 
from BetCalc import *
from DataParser import *


class Player:
    def run(self, input_socket):
        f_in = input_socket.makefile()

        # amount bet after flop / 200 - percentage of hand/board
        # cut off for accepting my bets: my bets/200  - percentage of hand/board
        # preflop bet /200 - percentage of starting hand

        # global variables
        d = DataParser()
        minOppPercent = 100 # minimum percept opp goes all in on 
        discardRound = 0 # 0 if preflop, 1 if preturn, 2 if preriver
        quitWhileAheadMode = False
        winMode = False
        onEdgeMode = False
        quitRank = 52 # max rank to call in quitwhileaheadmode
        myStack = 200
        myBank = 0
        handID = 1
        numHands = 1000
        bc = BetCalc()

        
        while True:
            data = f_in.readline().strip()
            if not data:
                print "Gameover, engine disconnected."
                break
            print data

        # QUIT WHILE YOU'RE AHEAD FUNCTION ! **************
            quitWhileAheadMode =  myBank > myStack
            winMode = myBank > 1.5*(numHands-handID)
            onEdgeMode = myBank < handID-numHands
            #print quitWhileAheadMode
            if winMode:
                s.send("CHECK\n")
                continue

            d.parse(data)

            word = d.word

            if word == "NEWGAME":
                myStack = d.stackSize
                numHands = d.numHands
            elif word == "NEWHAND":
                myBank = d.myBank
                startingHandRank = d.startingHandRank
                handID = d.handID
            elif word == "GETACTION":

                actionType = d.actionType
                handRank = d.handRank

                # opponent checked
                if actionType == "CHECK BET/RAISE":
                    if len(d.board) == 0:  # range for preflop: 61 to 40
                        bettingNums = [70, # preflop, go all in 
                                       70, # preflop, large bet/raise
                                       54, # preflop, medium bet/raise
                                       53] # preflop, small bet/raise
                    else:
                        bettingNums = [90, # postflop, go all in 
                                       85, # postflop, large bet/raise
                                       75, # postflop, medium bet/raise
                                       70] # postflop, small bet/raise 
                    if (quitWhileAheadMode or onEdgeMode) and handRank < quitRank and len(d.board) == 0:
                        s.send("FOLD\n")
                    elif handRank >= bettingNums[0]: # all in
                        s.send(d.betOrRaise+":"+str(d.maxBet)+"\n")
                    elif handRank >= bettingNums[1]:
                        bet = bc.getBetAmount("LARGE",d.maxBet,d.minBet)
                        s.send(d.betOrRaise+":"+str(bet)+"\n")
                    elif handRank >= bettingNums[2]:
                        bet = bc.getBetAmount("MED",d.maxBet,d.minBet)
                        s.send(d.betOrRaise+":"+str(bet)+"\n")
                    elif handRank >= bettingNums[3]:
                        bet = bc.getBetAmount("SMALL",d.maxBet,d.minBet)
                        s.send(d.betOrRaise+":"+str(bet)+"\n")
                    else:
                        s.send(d.betOrRaise+":"+str(d.minBet)+"\n") 

                # discard round
                elif actionType == "CHECK DISCARD DISCARD":
                    s.send(d.shouldDiscard)

                # opponent bet and it wasnt all-in
                elif actionType == "FOLD CALL RAISE" or actionType == "FOLD CALL": 
                    if len(d.board) == 0:
                        bettingNums = [54, # preflop, rank to raise on a bet
                                       50] # preflop, rank to call a bet
                    else:
                        bettingNums = [90, # postflop, rank to raise on a bet
                                       85] # postflop, rank to call a bet
                    # quit while youre ahead!
                    if (quitWhileAheadMode or onEdgeMode) and handRank < quitRank and len(d.board) == 0:
                        s.send("FOLD\n")
                    # raise!
                    elif handRank >= bettingNums[0] and actionType != "FOLD CALL":
                        raiseAmount = d.maxRaise/2.0+d.minRaise/2.0 # good amount?
                        s.send("RAISE:"+str(raiseAmount)+"\n") 
                    # call no matter what
                    elif handRank >= bettingNums[1]:
                        s.send("CALL\n")
                        print "handRank threshold call"
                    # call big bet
                    elif len(d.board) == 0:
                        s.send("FOLD\n")
                    #elif handRank >= bettingNums[1] and d.oppBet >= myStack/2.0:
                    #elif handRank >= bettingNums[1] and d.oppBet >= myStack/4.0:
                    else:

                        # FOLD MORE OFTEN TO DEFEAT FORD
                        # FOLD LESS OFTEN TO DEFEAT BLUFFBOT
                        
                        if d.oppBet <= d.handRank/3:
                            print "betsize 1 call"
                            s.send("CALL\n")

                        elif d.potSize - d.oppBet >= d.oppBet: 
                            print "betsize 2 call"
                            s.send("CALL\n")
                        else:
                            s.send("FOLD\n")
# shitty hand (30% ish)
# raise on pre flop
# what to do?
# -> usually a good hand

#pokerbots
# protect card for hopeful straight (50% chance) in discard method

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
