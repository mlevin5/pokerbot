from deuces.deuces import Card, Evaluator
from myCard import * 
from SetOfCards import *



def evalCards(myCardList):
	evalCards = []
	for card in myCardList:
		evalCards.append(card.evalCard)
	return evalCards

class PercentWin:
	def __init__(self, board, hand):
		self.board = board
		self.hand = hand

		self.evalBoard = evalCards(board)
		self.evalHand = evalCards(hand)

		self.evaluator = Evaluator()
		
		self.availableCards = []
		for suit in ["d","c","s","h"]:
			for val in ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]:
				availCard = myCard(val+suit)
				if not availCard in self.hand+self.board:
					self.availableCards.append(availCard)
		self.handDict = dict()
		self.discardDict = dict()
		#print self.availableCards

	def addToBoard(self, card):
		self.board.append(card)
		self.evalBoard.append(card.evalCard)
		self.availableCards.remove(card)
		#print self.availableCards
	def updateHand(self, oldCard, newCard):
		self.hand.remove(oldCard)
		self.hand.append(newCard)
		self.evalHand = evalCards(self.hand)
		self.availableCards.remove(newCard)

	# dont do this when board is zero
	def getWinPercentage(self):
		setOfCards = SetOfCards(self.hand, self.board)
		if len(self.board) >= 3 and not setOfCards in self.handDict:
			myHandRank = self.evaluator.evaluate(self.evalBoard, self.evalHand)
			#print myHandRank, self.board, self.hand
			possibleOppHand = []
			numWinsForMe = 0
			total = 0
			for handCard1 in self.availableCards:
				for handCard2 in self.availableCards:
					if not handCard1 == handCard2:

						possibleOppHand = [handCard1.evalCard, handCard2.evalCard]
						thisHandRank = self.evaluator.evaluate(self.evalBoard, possibleOppHand)
						#print total, thisHandRank, self.board, handCard1, handCard2
						if thisHandRank >= myHandRank:
							numWinsForMe+=1					
						total+=1
			handPer = ( float(numWinsForMe)/total ) * 100
			self.handDict[setOfCards] = handPer
			return handPer
		# starting hand
		elif len(self.board) == 0 and not setOfCards in self.handDict:
			f = open("startinghanddata.txt","r")
			myHandSameSuit = self.hand[0].suit == self.hand[1].suit
			while True:
				lineList = f.readline().strip().split()
				if lineList == []:
					break
				handStr = lineList[1].upper()
				if (self.hand[0].face.upper() in handStr and self.hand[1].face.upper() in handStr):
					if myHandSameSuit and handStr[-1] == "S":
						self.startingHandRank = float(lineList[3]) * 100
						return self.startingHandRank
					elif not myHandSameSuit and not handStr[-1] == "S":
						self.startingHandRank = float(lineList[3]) * 100
						return self.startingHandRank
			return 0
		if setOfCards in self.handDict:
			self.startingHandRank = self.handDict[setOfCards]
			return self.startingHandRank
		else:
			return 0

	def shouldDiscard_old(self, handPercentWin):
		setOfCards = SetOfCards(self.hand, self.board)
		if not setOfCards in self.discardDict:
			newHandDiscard1 = []
			numWinsForNewHand1 = 0
			numWinsForNewHand2 = 0
			total = 0
			for newBoardCard in self.availableCards:
				self.board.append(newBoardCard)
				self.evalBoard.append(newBoardCard.evalCard)
				self.availableCards.remove(newBoardCard)
				myHandRank = self.evaluator.evaluate(self.evalBoard, self.evalHand)
				print myHandRank
				for replacementCard in self.availableCards:
					if (newBoardCard != replacementCard and 
						self.hand[0] != replacementCard and 
						self.hand[1] != replacementCard):

						newHandDiscard1 = [self.hand[0].evalCard, replacementCard.evalCard]
						newHandDiscard2 = [self.hand[1].evalCard, replacementCard.evalCard]

						thisHandRank1 = self.evaluator.evaluate(self.evalBoard, newHandDiscard1)
						thisHandRank2 = self.evaluator.evaluate(self.evalBoard, newHandDiscard2)
						print newHandDiscard2, thisHandRank2
						print newHandDiscard1, thisHandRank1
						if thisHandRank1 >= myHandRank:
							numWinsForNewHand1+=1			
						if thisHandRank2 >= myHandRank:
							numWinsForNewHand2+=1				
						total+=1
				self.board.remove(newBoardCard)
				self.evalBoard.remove(newBoardCard.evalCard)
				self.availableCards.append(newBoardCard)
			if numWinsForNewHand1 >= numWinsForNewHand2:
				discard = self.hand[0]
				discardPercent = (float(numWinsForNewHand1)/total)*100
			else:
				discard = self.hand[1]
				discardPercent = (float(numWinsForNewHand2)/total)*100
			self.discardDict[setOfCards] = discardPercent
		else:
			discardPercent = self.discardDict[setOfCards]
		
		print discardPercent
		if discardPercent > handPercentWin:
			return "DISCARD:"+discard.strCard+"\n"
		else:
			return "CHECK\n" 

	def shouldDiscard(self, handPercentWin):
		myHandRank = self.evaluator.evaluate(self.evalBoard, self.evalHand)
		discardPercent = []
		for card in self.hand:
			setOfCards = SetOfCards([card], self.board)
			if setOfCards in self.discardDict:
				discardPercent.append(self.discardDict[setOfCards])
			else:
				print card
				discardPercent.append(self.discardLoop(card, myHandRank))
		if discardPercent[0] >= handPercentWin:
			return "DISCARD:"+self.hand[1].strCard+"\n"
		elif discardPercent[1] >= handPercentWin:
			return "DISCARD:"+self.hand[0].strCard+"\n"
		elif discardPercent[1] >= discardPercent[0] and handPercentWin <= 50.0:
			return "DISCARD:"+self.hand[0].strCard+"\n"
		elif discardPercent[0] >= discardPercent[1] and handPercentWin <= 50.0:
			return "DISCARD:"+self.hand[1].strCard+"\n"
		else:
			return "CHECK\n" 


	def discardLoop(self, handCard, myHandRank):
		numWinsForNewHand = 0
		total = 0
		for replacementCard in self.availableCards:
			if handCard != replacementCard:
				newHandDiscard = [handCard.evalCard, replacementCard.evalCard]
				thisHandRank = self.evaluator.evaluate(self.evalBoard, newHandDiscard)
				if thisHandRank <= myHandRank:
					numWinsForNewHand += 1
				total+=1		

		discardPercent = (numWinsForNewHand / float(total)) * 100
		self.discardDict[SetOfCards([],[handCard]+self.board)] = discardPercent

		return discardPercent


# FIX THIS ONE PART OF THIS:
# KEEP A VERY STRONG STARTING HAND ~ALMOST~ NO MATTER WHAT
"""
Dealt to challenger_theinnermachinat [9d Jc]
opponent_awp calls
challenger_theinnermachinat raises to 35
opponent_awp calls
*** FLOP *** (70) [Ts Kd Ad]
"""

def main():
	pw1 = PercentWin([myCard("Ts"),myCard("Kd"),myCard("Ad")],
		[myCard("Td"),myCard("Jc")])
	pw2 = PercentWin([],[myCard("8d"), myCard("Jd")])
	handRank =  pw1.getWinPercentage()
	print handRank
	print pw1.shouldDiscard(handRank)
main()


					



