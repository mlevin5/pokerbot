import random

class BetCalc:
	def getBetAmount_new(self, betType, maxBet, minBet):
		maxBet = int(maxBet)
		minBet = int(minBet)
		if maxBet <= minBet:
			return maxBet
		if betType == "SMALL":
			bet = random.randint(minBet, maxBet/4)
		elif betType == "MED":
			bet = random.randint(minBet/4, maxBet/2)
		elif betType == "LARGE":	
			bet = random.randint(minBet/2, maxBet)
		if bet < minBet:
			bet = minBet
		elif bet > maxBet:
			bet = maxBet

		return bet
			

	def getBetAmount(self, betType, maxBet, minBet):
		LoUpper = 0.06
		LoInside = 0.7

		MedLower = 0.1
		MedUpper = 0.2
		MedInside = 0.6
		MedOutLo = 0.1
		MedOutHi = 0.3

		HiPoint = 0.3
		HiAbove = 0.95
		HiBelow = 0.05
		HiAllIn = 0.1

		# Sigma values may need to be adjusted.

		# will only ever go up to 0.5
		LoSigma = (1.0/3.0) * (0.5 - LoUpper)
		# in between 0 and MedLower
		MedSigmaLo = (1.0/3.0) * (MedLower)
		# will only ever go up to 0.75
		MedSigmaHi = (1.0/3.0) * (0.75 - MedUpper)
		# can go up to all in bb
		HiSigmaHi =  (1.0/3.0) * (1 - HiPoint)
		# in between 0 and HiPoint
		HiSigmaLo = (1.0/3.0) * (HiPoint)

		if maxBet < minBet:
			return maxBet
		percentile = random.random()
		if betType == "SMALL":
			if percentile < LoInside: #
				percentile = random.random() * LoUpper #
			else:
				percentile = LoUpper + abs(random.gauss(0, LoSigma)) 
		elif betType == "MED":
			if percentile < MedInside: #
				percentile = MedLower + (random.random() * (MedUpper - MedLower)) 
			elif percentile < MedInside + MedLower:
				percentile = MedLower - abs(random.gauss(0, MedSigmaLo))
			else:
		 		percentile = MedUpper + abs(random.gauss(0, MedSigmaHi))
		elif betType == "LARGE":	
			if percentile < HiAbove:
				percentile = HiPoint + abs(random.gauss(0, HiSigmaHi))
			else:
				percentile = HiPoint - abs(random.gauss(0, HiSigmaLo))
		
		finalBet = percentile * maxBet

		if finalBet < minBet:
			finalBet = minBet
		elif finalBet > maxBet:
			finalBet = maxBet

		return finalBet
