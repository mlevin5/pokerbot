class Action:
	def __init__(self, actionStr):
		splits = actionStr.split(":")
		self.action = splits[0]
		if len(splits) == 3:
			self.amount = splits[1]
		elif len(splits) == 4: # can be SHOW or DISCARD
			self.card1 = splits[1] # old card if DISCARD
			self.card2 = splits[2] # new card if DISCARD
		if self.action == "DEAL":
			self.stage = splits[-1]
		else:
			self.player = splits[-1]
def main():
	action = Action("DEAL:FLOP")
	print action.stage
#main()
