from deuces.deuces import Card, Evaluator

class myCard:
	def __init__(self, strCard):
		self.strCard = strCard
		self.evalCard = Card.new(strCard)
		self.face = strCard[0]
		self.suit = strCard[1]

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.strCard == other.strCard
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	#self is less than other
	def __lt__(self, other):
		if isinstance(other, self.__class__):
			vals = {"T": 10,
					"J": 11,
					"Q": 12,
					"K": 13,
					"A": 14}
			if self.strCard[0].isdigit():
				selfcard = int(self.strCard[0])
			else:
				selfcard = vals[self.strCard[0]]
			if other.strCard[0].isdigit():
				othercard = int(other.strCard[0])
			else:
				othercard = vals[other.strCard[0]]	
			return selfcard < othercard
		else:
			return False

	def __gt__(self, other):
		return not self.__lt__(other) and self.strCard[0] != other.strCard[0]

	def __str__(self):
		return self.strCard
	def __repr__(self):
		return self.__str__()

def main():
	assert myCard("4d") < myCard("5s")
	assert not (myCard("5d") > myCard("5s"))
	assert myCard("As") > myCard("6d")
main()