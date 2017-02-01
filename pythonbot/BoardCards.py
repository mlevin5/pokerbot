class BoardCards:
	def __init__(self, boardCards):
		self.boardCards = boardCards

	def append(self, card):
		self.boardCards.append(card)
    # is it the exact same hand?
	def equals(self, hand):
		return 0
	# is it the equivalent hand (same suit / offsuit) ?
	def equiv(self, hand):
		return False

	def howManyCards(self):
		return self.boardCards.length()
	def getRank(self):
		return 0


def main():
	return 0
main()
