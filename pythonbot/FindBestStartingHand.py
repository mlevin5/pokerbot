from myCard import * 
from SetOfCards import *
from StartingHand import *

class FindBestStartingHand:	
	def parse(self):
		f = open("potnetdata.txt","r")
		Q6 = False
		hands = {}
		dealt = {}
		lines = True

		while lines:
			lineList = f.readline().strip().split()
			if lineList == []:
				pass
			elif lineList[0] == "FINAL:":
				lines = False
				break
			elif lineList[0] == "Dealt":
				hand = StartingHand(myCard(lineList[3][1:]),myCard(lineList[4][:-1]))
				dealt[lineList[2]] = hand
			elif lineList[1] == "wins" and lineList[4] == "(400)":
				for player in dealt:
					hand = dealt[player]
					if hand in hands:
						hands[hand][1] += 1
					else:
						hands[hand] = [0,1] # 0 wins, 1 appearance total
				winningHand = dealt[lineList[0]]
				hands[winningHand][0] += 1

		items = hands.items()
		sorted_items = sorted(items, key=lambda x: x[1][0]/float(x[1][1]), reverse=True)
		for hand, info in sorted_items:
			rank = info[0]/float(info[1])
			print "HAND:", hand, "RANK:", rank

		#print hands
		print len(hands) # should be 169
		return hands
def main():
	f = FindBestStartingHand()
	f.parse()
#main()






