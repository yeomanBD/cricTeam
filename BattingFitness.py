import numpy as np
import pandas as pd 
import random as rn 
import math

'''Coding section for loading data'''

inningsData = pd.read_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\BangladeshT20IBattingInnings.csv')

players = set(inningsData['Player'])

# Runs of all players #
Runs = []
for i in range(len(inningsData['Runs'])):
	run = inningsData['Runs'][i]
	if run == 'DNB':
		Runs.append(-1)
	elif '*' in run:
		Runs.append(int(run[:-1]))
	else:
		Runs.append(int(run))

# Batting Point for all players #
BP = []
for i in range(len(Runs)):
	run = Runs[i]
	ball = inningsData['BF'][i]
	if run == -1 or int(ball)==0:
		BP.append('Nan')
	else:
		BP.append(run * (run/int(ball)))

#print(BP)
#inningsData['BP'] = BP
#inningsData.to_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\BangladeshT20IBattingInningsBP.csv',index=False)
inningsDataBP = pd.read_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\BangladeshT20IBattingInningsBP.csv')

inningsDataR = pd.read_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\BangladeshT20BattingRecent.csv')

#print(inningsDataBP['Start Date'])

def playerRecentAvrg():
	PlayerSerialBP = {}
	for player in players:
		serial = {inningsDataR['Serial'][i]:inningsDataR['BP'][i] for i in range(len(inningsDataR)) if inningsDataR['Player'][i]==player}
		ball = {inningsDataR['Serial'][i]:inningsDataR['Runs'][i] for i in range(len(inningsDataR)) if inningsDataR['Player'][i]==player}
		s = sorted(serial,reverse=True)
		count = 0; total = 0;innin = 0
		if len(s)==0:
			PlayerSerialBP[player] = 0
		else:
			for i in range(len(s)):
				run = ball[s[i]]
				if '*' in run and int(run[:-1])<20:
					total += serial[s[i]]*(.96)**i
				else:
					total += serial[s[i]]*(.96)**i
					count += (.96)**i
					innin += 1
			if innin < 5:
				PlayerSerialBP[player] = (total/count)*(innin/5)
			else:
				PlayerSerialBP[player] = total/count

	return PlayerSerialBP

#def playerRecentPoint():

def playerRecentFour():

	rFourPoint = {}
	for player in players:
		fours = sum([ int(inningsDataR['4s'][i])  for i in range(len(inningsDataR)) if inningsDataR['Player'][i]==player])
		balls = sum([ int(inningsDataR['BF'][i])  for i in range(len(inningsDataR)) if inningsDataR['Player'][i]==player])

		if balls == 0:
			rFourPoint[player] = 0
		else:
			if fours < 10:
				rFourPoint[player] = 10 * ((10*fours)/balls) * (fours/10)
			else:
				rFourPoint[player] = 10 * ((10*fours)/balls)

	return rFourPoint


def playerRecentSix():

	rFourPoint = {}
	for player in players:
		fours = sum([ int(inningsDataR['6s'][i])  for i in range(len(inningsDataR)) if inningsDataR['Player'][i]==player])
		balls = sum([ int(inningsDataR['BF'][i])  for i in range(len(inningsDataR)) if inningsDataR['Player'][i]==player])

		if balls == 0:
			rFourPoint[player] = 0
		else:
			if fours < 5:
				rFourPoint[player] = 15 * ((25*fours)/balls) * (fours/5)
			else:
				rFourPoint[player] = 15 * ((25*fours)/balls)

	return rFourPoint

#print(playerRecentSix())
recentStrik = pd.read_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\SRwithoutboundaryBangladeshBattingRecent.csv')
def RecentSinglePoint():
	recentSingle = {}
	playerR = {recentStrik['Player'][i]:recentStrik['Single Points'][i] for i in range(len(recentStrik))}
	for player in players:
		if player in playerR:
			recentSingle[player] = playerR[player]
		else:
			recentSingle[player] = 0

	return recentSingle

'''

#print(RecentSinglePoint())
playerRA = playerRecentAvrg()
playerF = playerRecentFour()
playerSi = playerRecentSix()
playerS = RecentSinglePoint()
def recentTotalPoints():
	recentPoint = {}
	for player in players:
		recentPoint[player] = playerRA[player] + playerS[player]+playerF[player]+playerSi[player]

	return recentPoint

rTotal = recentTotalPoints()

pRA = []; pF = []; pSi = []; pS = []; pRT = []
for player in players:
	pRA.append(playerRA[player])
	pF.append(playerF[player])
	pSi.append(playerSi[player])
	pS.append(playerS[player])
	pRT.append(rTotal[player])

dataF = {#'Players':Players,
		'Avrg Point':pRA,
		'Four Point':pF,
		'Six Point':pSi,
		
		'Single Point':pS,
		
		'Carrier Point':pRT}

'''
#carrierP = pd.DataFrame(dataF,index=players)

#carrierP.to_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\FinalFiles\\BatsmanRecentPoint.csv',index=players)



def getRunByPlayer(player):
	runs = []
	for i in range(len(inningsData)):
		if inningsData['Player'][i]==player:
			runs.append(inningsData['Runs'][i])
	return runs

def getInnings():
	innings = {}
	for player in players:
		runs = getRunByPlayer(player)
		count = 0
		for run in runs:
			if run == 'DNB':
				continue
			elif '*' in run and int(run[:-1]) < 20:
				continue
			else:
				count += 1

		innings[player] = count
	return innings

Innings = getInnings()

#print(Innings)

def BPAvg():
	BPavg = {}
	for player in players:
		bp = [inningsDataBP['BP'][i] for i in range(len(inningsDataBP)) if inningsDataBP['Player'][i]==player]
		totalBP = sum([float(i) for i in bp if i != 'Nan'])
		if Innings[player] != 0:
			BPavg[player] = totalBP/Innings[player]
		else:
			BPavg[player] = 0
	return BPavg

BPavg = BPAvg()
#print(BPavg)

def standardDeviation():
	SD = {}
	for player in players:
		runs = getRunByPlayer(player)
		bp = [float(inningsDataBP['BP'][i]) for i in range(len(inningsDataBP)) if inningsDataBP['Player'][i]==player]
		BPPlayer = 0
		count = 0
		for i in range(len(runs)):
			run = runs[i]
			if run == 'DNB':
				continue
			elif '*' in run and int(run[:-1]) > 20:
				BPPlayer += (bp[i]-BPavg[player])**2
				count += 1
			else:
				BPPlayer += (bp[i]-BPavg[player])**2
				count+=1
		if count <= 4:
			SD[player] = 0
		else:
			#print(player,BPPlayer,count)
			SD[player] = math.sqrt(BPPlayer/(count - 1))

	return SD	 

SD = standardDeviation()
#print(SD)

def consistency():
	PlayerConsistency = {} 
	for player in players:
		sd = SD[player]
		if sd == 0:
			PlayerConsistency[player] = 0
		else:
			#PlayerConsistency[player] = 10 * (BPavg[player]/SD[player])
			PlayerConsistency[player] = (BPavg[player]/SD[player])

	return PlayerConsistency

PlayerConsistency = consistency()

avbp = []; sd = []; con = [];
for player in players:
	avbp.append(BPavg[player])
	sd.append(SD[player])
	con.append(PlayerConsistency[player])

d = {'Player':list(players),
	 'AvrgBP':avbp,
	 'SD' : sd,
	 'Consistency':con
}
data = pd.DataFrame(d,index = list(players))
data.to_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\FinalFiles\\AVRGSDC.csv',index=list(players))

'''

def fourPoint():
	FourPoint = {}
	for player in players:
		fours = [inningsData['4s'][i] for i in range(len(inningsData['4s'])) if inningsData['Player'][i]==player]
		ball = [inningsData['BF'][i] for i in range(len(inningsData['BF'])) if inningsData['Player'][i]==player]

		totalFour = sum([int(i) for i in fours if i != '-'])
		totalBall = sum([int(i) for i in ball if i != '-'])	

		if totalBall == 0:
			FourPoint[player] = 0
		elif totalFour >= 20:
			FourPoint[player] = 10 * ((10*totalFour)/totalBall)
		else:
			FourPoint[player] = 10 * ((10*totalFour)/totalBall)*(totalFour/20)

	return FourPoint

def SixPoint():
	FourPoint = {}
	for player in players:
		fours = [inningsData['6s'][i] for i in range(len(inningsData['6s'])) if inningsData['Player'][i]==player]
		ball = [inningsData['BF'][i] for i in range(len(inningsData['BF'])) if inningsData['Player'][i]==player]

		totalFour = sum([int(i) for i in fours if i != '-'])
		totalBall = sum([int(i) for i in ball if i != '-'])	

		if totalBall == 0:
			FourPoint[player] = 0
		elif totalFour >= 10:
			FourPoint[player] = 15 * ((25*totalFour)/totalBall)
		else:
			FourPoint[player] = 15 *  ((25*totalFour)/totalBall)*(totalFour/10)

	return FourPoint


partnershipData = pd.read_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\BangladeshT20IPartnerships.csv')

def noOfBatting():
	NoOfBats = {}
	for player in players:
		NoOfBats[player] = sum([1 for i in range(len(inningsData)) if inningsData['Player'][i]==player and inningsData['Runs'][i]!='DNB'])
	return NoOfBats

def numberOfPartner():
	noOfPertnerShip = {}
	for player in players:
		count = 0
		for i in range(len(partnershipData)):
			if player in partnershipData['Partners'][i]:
				count += partnershipData['Inns'][i]

		noOfPertnerShip[player] = count

	return noOfPertnerShip

def partnerShipPoint():
	partnerShipPoint = {}
	Innings = noOfBatting()
	partnerShip = numberOfPartner()
	for player in players:
		if Innings[player] == 0:
			point = 0
		else:
			point = 5 * (partnerShip[player]/Innings[player])

		partnerShipPoint[player] = point 
	return partnerShipPoint

#partnershipPoint = partnerShipPoint()
#print(partnershipPoint)

SingleStrikeRate = pd.read_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\BangladeshT20IBattingSingleStrikeRate.csv')

def singleStrikeRate():
	StrikeRate = {}
	for i in range(len(SingleStrikeRate)):
		StrikeRate[SingleStrikeRate['PlayerAscending'][i]] = SingleStrikeRate['SingleP'][i]

	return StrikeRate

'''
'''
avgBP = BPAvg()
consistent = consistency()
four = fourPoint()
six = SixPoint()
partner = partnerShipPoint()
singleP = singleStrikeRate()

#print(consistent)
def carrierPoints():
	CarrierPoint = {}
	for player in players:
		CarrierPoint[player] = avgBP[player]+consistent[player]+four[player]+six[player]+partner[player]+singleP[player]

	return CarrierPoint

#print(carrierPoints())


#inningsData.to_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\BangladeshT20IBattingInningsBP.csv',index=False)
ABP = []; C = []; FP = []; SP = []; PP = []; SiP = []; CP = [];
Players = list(players)
CarrierPoint = carrierPoints()
for player in Players:
	ABP.append(avgBP[player])
	C.append(consistent[player])
	FP.append(four[player])
	SP.append(six[player])
	PP.append(partner[player])
	SiP.append(singleP[player])
	CP.append(CarrierPoint[player])

#print(len(Players),len(ABP),len(C),len(FP),len(SP),len(PP),len(CP))
dataF = {#'Players':Players,
		'Avrg Point':ABP,
		'Four Point':FP,
		'Six Point':SP,
		'Partner Point':PP,
		'Single Point':SiP,
		'Consistency':C,
		'Carrier Point':CP}


carrierP = pd.DataFrame(dataF,index=Players)

carrierP.to_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\BatsmanPoint.csv',index=Players)

'''