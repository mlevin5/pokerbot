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

	def shouldDiscard(self, handPercentWin):
		myHandRank = self.evaluator.evaluate(self.evalBoard, self.evalHand)
		discardPercent = []
		protect = []
		for card in self.hand:
			setOfCards = SetOfCards([card], self.board)
			if setOfCards in self.discardDict:
				discardPercent.append(self.discardDict[setOfCards])
			else:
				discardData = self.discardLoop(card, myHandRank)
				discardPercent.append(discardData[0])
				protect.append(discardData[1])
		if protect[0]:
			discardPercent[1] = 0.0
		if protect[1]:
			discardPercent[0] = 0.0
		discPercs = [(discardPercent[1], self.hand[0]),
					 (discardPercent[0], self.hand[1])]
		print discPercs
		if discPercs[0][0] > discPercs[1][0]:
			discardThisCard = discPercs[0]
		elif discPercs[0][0] < discPercs[1][0]:
			discardThisCard = discPercs[1]
		elif discPercs[0][1] < discPercs[1][1]:
			discardThisCard = discPercs[0]
		else:
			discardThisCard = discPercs[1]
		if discardThisCard[0] <= 50.0:
			return "CHECK\n"
		elif discardThisCard[0] >= 80.0 or discardThisCard[0] >= handPercentWin or handPercentWin <= 50.0:
			return "DISCARD:"+discardThisCard[1].strCard+"\n"
		else:
			return "CHECK\n"


	def discardLoop(self, handCard, myHandRank):
		print myHandRank
		numWinsForNewHand = 0
		total = 0
		protect = False
		for replacementCard in self.availableCards:
			if handCard != replacementCard:
				newHandDiscard = [handCard.evalCard, replacementCard.evalCard]
				thisHandRank = self.evaluator.evaluate(self.evalBoard, newHandDiscard)
				print thisHandRank, replacementCard, handCard
				if thisHandRank <= 1609:
					protect = True
				if thisHandRank - 3 <= myHandRank:
					numWinsForNewHand += 1
				total+=1		# 7642
		discardPercent = (numWinsForNewHand / float(total)) * 100

		self.discardDict[SetOfCards([],[handCard]+self.board)] = discardPercent
		return [discardPercent, protect]


# FIX THIS ONE PART OF THIS:
# KEEP A VERY STRONG STARTING HAND ~ALMOST~ NO MATTER WHAT
"""
*** TURN *** (400) [9d Qs Ks] [2h]
8c kc
"""

def main():
	pw1 = PercentWin([myCard("9c"),myCard("Qs"),myCard("Ks"),myCard("2h")],
		[myCard("8c"),myCard("Kc")])
	# worst straight: 1609
	# best straight: 1600
	# worst flush: 1599
	# best flush: 323
	# worst straight flush: 9
	# best straight flush: 1
	pw2 = PercentWin([],[myCard("8d"), myCard("Jd")])
	handRank =  pw1.getWinPercentage()
	print handRank, "handRank"
	print pw1.shouldDiscard(handRank)
main()


					



