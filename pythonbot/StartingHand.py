class StartingHand:
	def __init__(self, card1, card2, suit1 = None, suit2 = None, sameSuit = None):

		self.card1 = card1
		self.suit1 = suit1

		self.card2 = card2
		self.suit2 = suit2

		if suit1 == None and suit2 == None:
			self.sameSuit = sameSuit
		else:
			self.sameSuit = self.suit1 == self.suit2

	# is it the equivalent hand (same suit / offsuit) ?
	def equiv(self, hand):
		p1 = hand.getCard1() == self.getCard1() and hand.getCard2() == self.getCard2()
		p2 = hand.getCard2() == self.getCard1() and hand.getCard1() == self.getCard2()
		if p1 or p2:
			p3 = hand.isSameSuit() and self.isSameSuit()
			p4 = not hand.isSameSuit() and not self.isSameSuit()
			return p3 or p4
		else:
			return False

	def isSameSuit(self):
		return self.sameSuit
	def getSuit1(self):
		return self.suit1
	def getSuit2(self):
		return self.suit2
	def getCard1(self):
		return self.card1
	def getCard2(self):
		return self.card2

	def getRank(self):
		f = open("startingHandRanks.txt","r")
		while True:

			lineList = f.readline().strip().split()
			if lineList == []:
				break
			handStr = lineList[0]

			hand = StartingHand(handStr[0],handStr[1], sameSuit = handStr[-1] == "s")

			if self.equiv(hand):
				return float(lineList[1])
		return 0


def main():
	hand = StartingHand("Q","6","h","s")
	print(hand.getRank())
	return 0
main()
