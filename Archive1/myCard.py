from deuces.deuces import Card, Evaluator

class myCard:
	def __init__(self, strCard):
		self.strCard = strCard
		self.evalCard = Card.new(strCard)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.strCard == other.strCard
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):
		return self.strCard
	def __repr__(self):
		return self.__str__()