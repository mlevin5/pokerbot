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
			f = open("startingHandRanks.txt","r")
			myHandSameSuit = self.hand[0].suit == self.hand[1].suit
			while True:
				lineList = f.readline().strip().split()
				if lineList == []:
					break
				handStr = lineList[0].upper()
				if (self.hand[0].face.upper() in handStr and self.hand[1].face.upper() in handStr):
					if myHandSameSuit and handStr[-1] == "S":
						self.startingHandRank = float(lineList[1])
						return self.startingHandRank
					elif not myHandSameSuit and not handStr[-1] == "S":
						self.startingHandRank = float(lineList[1])
						return self.startingHandRank
			return 0
		if setOfCards in self.handDict:
			self.startingHandRank = self.handDict[setOfCards]
			return self.startingHandRank
		else:
			return 0

	def shouldDiscard(self, handPercentWin):
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
				for replacementCard in self.availableCards:
					if (newBoardCard != replacementCard and 
						self.hand[0] != replacementCard and 
						self.hand[1] != replacementCard):

						newHandDiscard1 = [self.hand[0].evalCard, replacementCard.evalCard]
						newHandDiscard2 = [self.hand[1].evalCard, replacementCard.evalCard]

						thisHandRank1 = self.evaluator.evaluate(self.evalBoard, newHandDiscard1)
						thisHandRank2 = self.evaluator.evaluate(self.evalBoard, newHandDiscard2)

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

		if len(self.board) == 3 and self.startingHandRank > 60:
			return "CHECK\n" 
		elif discardPercent > handPercentWin:
			return "DISCARD:"+discard.strCard+"\n"
		else:
			return "CHECK\n" 

# FIX THIS ONE PART OF THIS:
# KEEP A VERY STRONG STARTING HAND ~ALMOST~ NO MATTER WHAT
	

def main():
	pw1 = PercentWin([myCard("Qc"),myCard("3h"),myCard("5d")],
		[myCard("Jh"),myCard("Ac")])
	pw2 = PercentWin([],[myCard("Jh"), myCard("Ac")])
	print pw2.getWinPercentage()
	
	#print pw.shouldDiscard(handRank)
main()


					



