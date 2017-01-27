class SetOfCards:
	def __init__(self, hand, board):
		self.list = hand+board

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			for card in self.list:
				if not card in other.list:
					return False
			return len(self.list) == len(other.list)
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(10)

	def __str__(self):
		return self.list
	def __repr__(self):
		return self.__str__()