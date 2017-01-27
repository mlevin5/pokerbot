import argparse
import socket
import sys

#from deuces.deuces import Card, Evaluator
from StartingHand import *
from PercentWin import *
from myCard import * 
from BetCalc import *


"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.
"""
class Player:
    def run(self, input_socket):

        minOppPercent = 100

        f_in = input_socket.makefile()
        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print "Gameover, engine disconnected."
                break

            print data

            d = data.split()
            word = d[0]
            if word == "NEWGAME":
                myName = d[1]
                oppName = d[2]
                stackSize = int(d[3]) # starting number of chips
                bb = int(d[4]) # big blind being used for the match (always a multiple of 2)
                numHands = int(d[5])
                timeBank = float(d[6]) # secs left for bot to return action
            if word == "KEYVALUE":
                key = d[1]
                value = d[2]
            if word == "NEWHAND":
                handID = int(d[1])
                # the button indicates the player who is set to act last after the cards are dealt
                button = bool(d[2]) # am i the button?
                card1 = d[3][0]
                suit1 = d[3][1]
                card2 = d[4][0]
                suit2 = d[4][1]
                startingHand = StartingHand(card1, card2, suit1, suit2)
                hand = [
                    myCard(card1+suit1),
                    myCard(card2+suit2)
                    ]
                board = []
                pw = PercentWin([], hand)
                bc = BetCalc()
                myBank = int(d[5])
                oppBank = int(d[6])
                timeBank = float(d[7])
            # GETACTION potSize numBoardCards [boardCards] numLastActions [lastActions] numLegalActions [legalActions] timebank
            if word == "GETACTION":
                potSize = int(d[1])

                numBoardCards = int(d[2])
                for i in range(0,numBoardCards):
                    if len(board) < numBoardCards:
                        newCard = myCard(d[2+numBoardCards-i])
                        board.append(newCard)
                        pw.addToBoard(newCard)

                numLastActions = int(d[3+numBoardCards])
                lastActions = []
                for j in range(0,numLastActions):
                    lastActions.append(d[4+numBoardCards+j])

                numLegalActions = int(d[4+numBoardCards+numLastActions])
                legalActions = []
                for k in range(0,numLegalActions):
                    legalActions.append(d[5+numBoardCards+numLastActions+k])
                timeBank = float(d[5+numBoardCards+numLastActions+numLegalActions])

                if lastActions[0][0] == "D": #discard
                    # update hand
                    parseDiscard = lastActions[0].split(":")
                    #print parseDiscard
                    oldHandCard = myCard(parseDiscard[1])
                    newHandCard = myCard(parseDiscard[2])
                    pw.updateHand(oldHandCard, newHandCard)

                if len(board) == 0:
                    handRank = startingHand.getRank()
                else:
                    handRank = pw.getWinPercentage()

               # print "\nHAND " , hand
               # print "\nBOARD " , board
               # print "\nRANK " , handRank ,"\n"

        # logic on bet i would accept 
        # / bet i would bet given the probability 

        # action calculator based on probability 



                if "CALL" in legalActions:
                    for action in legalActions:
                        if action[0] == "R": #raise
                            r = action.split(":")
                            minRaise = float(r[1])
                            maxRaise = float(r[2])
                            raiseAvail = True
                    oppBet = float(lastActions[-1].split(":")[1])

                    # print "\npotsize "+str(potSize)
                    # print "mybank "+str(myBank)
                    # when to raise
                    #print "handRank",handRank
                    #print "oppBet",oppBet
                    #print "potSize",potSize

                    if len(board) == 0 and raisingPreFlop/float(numHands) > 90.0:
                        if raiseAvail:
                            raisingPreFlop+=1
                        if handRank > 80.0:
                            s.send("CALL\n")
                        else:
                            s.fold("FOLD")

                    else:
                        if handRank >= 90.0 and raiseAvail:
                            s.send("RAISE:"+str(maxRaise/2.0+minRaise/2.0)+"\n") 
                        elif handRank >= 70.0:
                            s.send("CALL\n")
                        else:
                            if oppBet <= handRank*1.5:
                                s.send("CALL\n")
                            else:
                                s.send("FOLD\n")

                    raiseAvail = False
                else:
                    discardRound = False
                    if legalActions[1][0] == "D": #discard
                        discardRound = True
                    else:
                        r = legalActions[1].split(":")
                        minBet = float(r[1])
                        maxBet = float(r[2])

                       # print "handRank",handRank
                       # print "maxBet",maxBet
                       # print "potSize",potSize


                        # print minBet
                        # print maxBet
                    # should i discard a card???
                    if discardRound:
                        s.send(pw.shouldDiscard(handRank))
                    elif handRank >= 90:
                        bet = bc.getBetAmount("LARGE",maxBet,minBet)
                        s.send("BET:"+str(bet)+"\n")
                    elif handRank >= 75:
                        bet = bc.getBetAmount("MED",maxBet,minBet)
                        s.send("BET:"+str(bet)+"\n")
                    elif handRank >= 60:
                        bet = bc.getBetAmount("SMALL",maxBet,minBet)
                        s.send("BET:"+str(bet)+"\n")
                    else:
                        s.send("CHECK\n") 

            if word == "HANDOVER":
                myBank = int(d[1])
                oppBank = int(d[2])
                numBoardCards = int(d[3])
                #boardCards = BoardCards([])
                #for i in range(0,numBoardCards):
                #    boardCards.append(d[4+i])

                numLastActions = int(d[4+numBoardCards])
                lastActions = []
                for j in range(0,numLastActions):
                    lastActions.append(d[5+numBoardCards+j])

                if lastActions[2][0] == "S": # show
                    show = lastActions[2].split(":")
                    card1 = show[1][0]
                    suit1 = show[1][1]
                    card2 = show[2][0]
                    suit2 = show[2][1]
                    hand = [
                    myCard(card1+suit1),
                    myCard(card2+suit2)
                    ]
                    if potSize >= 200:
                        oppPercent = pw.getWinPercentage(hand, board)
                        minOppPercent = min(oppPercent,minOppPercent)

                timeBank = float(d[5+numBoardCards+numLastActions])


            elif word == "REQUESTKEYVALUES":
                bytesLeft = d[1] #num bytes left to store key/value pairs
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")


            # KEEPING TABS ON APP

            raisingPreFlop = 0


        # Clean up the socket.
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
