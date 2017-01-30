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
        myStack = 200
        myBank = 0
        bc = BetCalc()

        
        while True:
            data = f_in.readline().strip()
            if not data:
                print "Gameover, engine disconnected."
                break
            print data

        # QUIT WHILE YOU'RE AHEAD FUNCTION ! **************
            quitWhileAheadMode =  myBank >= myStack*1.5
            print quitWhileAheadMode

            d.parse(data)

            word = d.word

            if word == "NEWGAME":
                myStack = d.stackSize
            elif word == "NEWHAND":
                myBank = d.myBank
                startingHandRank = d.startingHandRank
            elif word == "GETACTION":

                actionType = d.actionType
                handRank = d.handRank

                if actionType == "CHECK BET/RAISE":
                    if len(d.board) == 0:
                        bettingNums = [80, 75, 70, 60]
                    else:
                        bettingNums = [97, 90, 80, 70]


                    if d.oppName[-6:] == "potnet":
                        s.send("RAISE:"+str(d.maxBet)+"\n")
                    elif quitWhileAheadMode:
                        if handRank >= bettingNums[0]:
                            s.send(d.betOrRaise+":"+str(d.maxBet)+"\n")
                        else:
                            s.send("CHECK\n")
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

                elif actionType == "CHECK DISCARD DISCARD":
                    s.send(d.shouldDiscard)

                    # CALL 95 IF NOTHING IN POT (400 is all in)
                    #(95, 400) -200/5x -3400
                    #(90, 200)
                    # CALL 90 IF SOMETHING ALREADY IN POT (198 is example)
                    # POT USUALLY SOMEWHAT PROPORTIONAL TO HOW GOOD THEIR CARD IS

                # needs to be fixed tbh
                elif actionType == "FOLD CALL RAISE": 
                    if len(d.board) == 0:
                        bettingNums = [75, 75, 50]
                    else:
                        bettingNums = [97, 90, 75]

                    if d.oppName[-6:] == "potnet":
                        s.send("RAISE:"+str(d.maxRaise)+"\n")
                    elif quitWhileAheadMode:
                        if handRank >= bettingNums[0]:
                            s.send("RAISE"+str(d.maxRaise)+"\n") 
                        else:
                            s.send("FOLD\n")
                    elif handRank >= bettingNums[1]:
                        print "raising"
                        s.send("RAISE:"+str(d.maxRaise/2.0+d.minRaise/2.0)+"\n") 
                    # calling 
                    elif handRank >= bettingNums[2]:
                        print "calling"
                        s.send("CALL\n")
                    else:
                        # this idea needs WERK
                        if d.oppBet <= d.handRank/3:
                            print "calling based on bet size"
                            s.send("CALL\n")
                        # elif d.potSize - d.oppBet >= d.stackSize/2.0
                        elif d.potSize - d.oppBet >= d.oppBet:
                            print "bet is small / ive already put a lot in"
                            s.send("CALL\n")
                        else:
                            print "folding"
                            s.send("FOLD\n")
# shitty hand (30% ish)
# raise on pre flop
# what to do?
# -> usually a good hand
                elif actionType == "FOLD CALL":
                    if len(d.board) == 0:
                        bettingNums = [70, 55]
                    else:
                        bettingNums = [97, 95]


                    if d.oppName[-6:] == "potnet":
                        if handRank >= 0.0:
                            s.send("CALL\n")
                        else:
                            s.send("FOLD\n")
                    elif quitWhileAheadMode:
                        if handRank >= bettingNums[0]:
                            s.send("CALL\n") 
                        else:
                            s.send("FOLD\n")
                    elif handRank >= bettingNums[1]:
                        print "calling"
                        s.send("CALL\n")
                    else:
                        s.send("FOLD\n")

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
