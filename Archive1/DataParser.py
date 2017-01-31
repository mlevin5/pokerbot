from StartingHand import *
from PercentWin import *
from myCard import * 
from BetCalc import *
from Action import *

class DataParser:
    def parse(self, data): 
        d = data.split()
        self.word = d[0]
        if self.word == "NEWGAME":
            self.myName = d[1]
            self.oppName = d[2]
            self.stackSize = int(d[3]) # starting number of chips
            self.bb = int(d[4]) # big blind being used for the match (always a multiple of 2)
            self.numHands = int(d[5])
            self.oppBet = self.bb
            #timeBank = float(d[6]) # secs left for bot to return action
        if self.word == "NEWHAND":
            #self.handID = int(d[1]) # number hand it is
            #self.button = bool(d[2]) # am i the button?
            card1 = d[3][0]
            suit1 = d[3][1]
            card2 = d[4][0]
            suit2 = d[4][1]
            self.startingHand = StartingHand(card1, card2, suit1, suit2)
            self.hand = [
                myCard(card1+suit1),
                myCard(card2+suit2)
                ]
            self.board = []
            self.pw = PercentWin([], self.hand)
            #self.bc = BetCalc()
            #self.myBank = int(d[5])
            #self.oppBank = int(d[6])
            # timeBank = float(d[7])
        # GETACTION potSize numBoardCards [boardCards] numLastActions [lastActions] numLegalActions [legalActions] timebank
        if self.word == "GETACTION":
            #self.potSize = int(d[1])
            numBoardCards = int(d[2])
            for i in range(0,numBoardCards):
                if len(self.board) < numBoardCards:
                    newCard = myCard(d[2+numBoardCards-i])
                    self.board.append(newCard)
                    self.pw.addToBoard(newCard)
            numLastActions = int(d[3+numBoardCards])
            lastActions = []
            for j in range(0,numLastActions):
                a = Action(d[4+numBoardCards+j])
                lastActions.append(a)
                if a.action == "BET":
                    if a.player == self.oppName:
                        self.oppBet = float(a.amount)
                elif a.action == "POST":
                    if a.player == self.oppName:
                        self.oppBet = float(a.amount)
                #if action.player == self.myName:
                #    if action.action == "BET":
                #        pass
                #    elif action.action == "RAISE":
                #        pass
            # amount bet after flop / 200 - percentage of hand/board
            # cut off for accepting my bets: my bets/200  - percentage of hand/board
            # preflop bet /200 - percentage of starting hand
               # if action.player == self.oppName:
               #     if action.action == "CALL":
               #         pass
               #     elif action.action == "BET":
                #        pass
               #     elif action.action == "RAISE":
               #         pass
               #     elif action.action == "DISCARD":
               #         pass
               #     elif action.action == "CHECK":
               #         pass
               #     elif action.action == "FOLD":
               #         pass

            numLegalActions = int(d[4+numBoardCards+numLastActions])
            legalActions = []
            for k in range(0,numLegalActions):
                legalActions.append(d[5+numBoardCards+numLastActions+k])
            #timeBank = float(d[5+numBoardCards+numLastActions+numLegalActions])

            # update hand if discarded a card last hand
            discard = lastActions[0]
            if discard.action == "DISCARD": #discard
                oldHandCard = myCard(discard.card1)
                newHandCard = myCard(discard.card2)
                self.pw.updateHand(oldHandCard, newHandCard)

            if len(self.board) == 0:
                self.handRank = self.startingHand.getRank()
            else:
                self.handRank = self.pw.getWinPercentage()


            # CHECK BET / CHECK RAISE
            if "CHECK" in legalActions and len(legalActions) == 2:
                r = legalActions[1].split(":")
                self.minBet = float(r[1])
                self.maxBet = float(r[2])
                self.actionType = "CHECK BET/RAISE"
                self.betOrRaise = r[0]

            # CHECK DISCARD DISCARD
            elif "CHECK" in legalActions and len(legalActions) == 3:
                self.actionType = "CHECK DISCARD DISCARD"
                self.shouldDiscard = self.pw.shouldDiscard(self.handRank)

            # FOLD CALL
            elif "CALL" in legalActions and len(legalActions) == 2:
                self.actionType = "FOLD CALL"
            # FOLD CALL RAISE
            elif "CALL" in legalActions and len(legalActions) == 3:
                r = legalActions[2].split(":")
                self.minRaise = float(r[1])
                self.maxRaise = float(r[2])
                for a in lastActions:
                    if a.action == "BET" and a.player == self.oppName:
                        self.oppBet = float(a.amount)
                self.actionType = "FOLD CALL RAISE"


        if self.word == "HANDOVER":
            self.myBank = int(d[1])
            self.oppBank = int(d[2])
            numBoardCards = int(d[3])
            numLastActions = int(d[4+numBoardCards])
            lastActions = []
            self.cardsShown = False
            for j in range(0,numLastActions):
                action = Action(d[5+numBoardCards+j])
                lastActions.append(action)
                if action.action == "WIN":
                    self.winner = action.player
                    self.winnersPot = action.amount
                if action.action == "SHOW" and action.player == self.oppName: 
                    self.cardsShown = True
                    self.oppEndHand = [ 
                    myCard(action.card1),
                    myCard(action.card2)
                    ]

           # timeBank = float(d[5+numBoardCards+numLastActions])




