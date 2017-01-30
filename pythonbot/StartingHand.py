from myCard import *

class StartingHand:
	def __init__(self, card1, card2):
		self.faces = [card1.face,card2.face]
		self.sameSuit = card1.suit == card2.suit

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			for card in self.faces:
				if not card in other.faces:
					return False
			return self.sameSuit == other.sameSuit
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(10)
	def __str__(self):
		s = self.faces[0]+self.faces[1]
		if self.sameSuit:
			return s+"s"
		else:
			return s
	def __repr__(self):
		return self.__str__()
def main():
	QTs = StartingHand(myCard("Qd"), myCard("Td"))
	QTs2 = StartingHand(myCard("Tc"), myCard("Qc"))
	QT = StartingHand(myCard("Qd"), myCard("Tc"))
	QT2 = StartingHand(myCard("Tc"), myCard("Qd"))
	QT3 = StartingHand(myCard("Qs"), myCard("Tc"))
	JT = StartingHand(myCard("Jd"), myCard("Tc"))
	assert QTs == QTs2
	assert QT == QT2
	assert QT2 == QT3
	assert QTs != QT
	assert JT != QT
main()