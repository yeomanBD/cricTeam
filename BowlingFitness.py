import numpy as np
import pandas as pd 
import random as rn 
import math

'''Coding section for loading data'''

inningsData = pd.read_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\FinalFiles\\BangladeshT20IBowlingBP.csv')

players = set(inningsData['Player'])

#print(inningsData)
def bowlingPoint():
	BP = []
	for i in range(len(inningsData)):
		if inningsData['Overs'][i] == 'DNB' or inningsData['Overs'][i] == 'TDNB':
			BP.append(0)
		else:
			o = float(inningsData['Overs'][i])
			over = int(o) + (o - int(o))*(10/6)
			run = int(inningsData['Runs'][i])
			wck = int(inningsData['Wkts'][i])
			point = run * (run/(over*6)) + ((20 - (wck*5)) * (over/4))
			BP.append(point)

	return BP

#inningsData['BP'] = bowlingPoint()
#inningsData.to_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\FinalFiles\\BangladeshT20IBowlingBP.csv',index=False)


def teamBP(date):
	total = 0
	totalOver = 0
	for i in range(len(inningsData)):
		if inningsData['Start Date'][i] == date:
			if inningsData['Overs'][i] == 'DNB' or inningsData['Overs'][i]=='TDNB':
				over = 0
			else:
				o = float(inningsData['Overs'][i])
				over = int(o) + (o - int(o))*(10/6)
				totalOver += over
				run = int(inningsData['Runs'][i])
	#			print(run)
				total += ((run**2)/(over*6))
	#print(total,totalOver)
	return (total/totalOver)

#print(teamBP('18-Sep-07'))

def qualityBowling():
	QB = []
	for i in range(len(inningsData)):
		if inningsData['Overs'][i] == 'DNB' or inningsData['Overs'][i]=='TDNB':
			QB.append(0)
		else:
			o = float(inningsData['Overs'][i])
			over = int(o) + (o - int(o))*(10/6)
			date = inningsData['Start Date'][i]
			point = over * ((inningsData['BP'][i]/over)-teamBP(date))
			QB.append(point)

	return QB	

#inningsData['Quality BP'] = qualityBowling()
#inningsData.to_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\FinalFiles\\BangladeshT20IBowlingP.csv',index=False)	

def avrgBPerOver():
	BP = []
	for i in range(len(inningsData)):
		if inningsData['Overs'][i] == 'DNB' or inningsData['Overs'][i]=='TDNB':
			BP.append(0)
		else:
			o = float(inningsData['Overs'][i])
			over = int(o) + (o - int(o))*(10/6)
			point = inningsData['BP'][i]/over
			BP.append(point)

	return BP

#inningsData['BPperOver'] = avrgBPerOver()
#inningsData.to_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\FinalFiles\\BangladeshT20IBowlingBP.csv',index=False)	

def getOver(player):
	o = 0
	for i in range(len(inningsData)):
		if player == inningsData['Player'][i]:
			if inningsData['Overs'][i] == 'DNB' or inningsData['Overs'][i]=='TDNB':
				continue
			else:
				ov = float(inningsData['Overs'][i])
				over = int(ov) + (ov - int(ov))*(10/6)
				o += over
	return o

def avrgBP():
	a = {}
	for player in players:
		bp = [inningsData['BP'][i] for i in range(len(inningsData)) if inningsData['Player'][i]==player]
		if len(bp) == 0:
			a[player] = 0
		else:
			over = getOver(player)
			a[player] = (sum(bp)*4)/over

	return a

#print(avrgBP())
	
def standard_deviation():
	sd = {}
	avBP = avrgBP()
	for player in players:
		bp = [float(inningsData['BP'][i]) for i in range(len(inningsData)) if inningsData['Player'][i]==player]
		count = 0;total = 0
		for i in bp:
			if i == 0:
				continue
			else:
				total += (i - avBP[player])**2
				count += 1
		
		if count <= 1:
			sd[player] = 0
		else:
			sd[player] = math.sqrt(total/(count-1)) 

	return sd

#print(standard_deviation())

def avrgBperover():
	a = {}
	for player in players:
		bp = [inningsData['BPperOver'][i] for i in range(len(inningsData)) if inningsData['Player'][i]==player]
		if len(bp) == 0:
			a[player] = 0
		else:
			a[player] = sum(bp)/len(bp)

	return a

def consistency():
	c = {}
	avrg = avrgBperover()
	sd = standard_deviation()
	for player in players:
		if avrg[player] == 0 or sd[player] == 0:
			c[player] = 0
		else:
			c[player] = 5 * (sd[player] / avrg[player])

	return c


C = pd.read_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\BangladeshT20IBowlingCombination.csv')

def com():
	c = {}
	for player in players:
		for i in range(len(C)):
			if player == C['Player'][i]:
				c[player] = C['Combination of Bowling'][i]
		

	return c

def qBP():
	q = {}
	for player in players:
		qbp = [float(inningsData['Quality BP'][i]) for i in range(len(inningsData)) if inningsData['Player'][i]==player]
		total = 0
		count = 0
		if len(qbp) == 0:
			q[player] = 0
		else:
			for i in qbp:
				if i == 0:
					continue
				else:
					total += i
					count += 1
		if count == 0:
			q[player] = 0
		else:
			q[player] = total/count
	return q

#print(qBP())

avBP = avrgBP()
avBperOver = avrgBperover()
sd = standard_deviation()
con = consistency()
com = com()
QB = qBP()

abp = []; abpo = []; std = []; cons = []; comb = []; qb = []; total = []
for player in players:
	abp.append(avBP[player])
	abpo.append(avBperOver[player])
	std.append(sd[player])
	cons.append(con[player])
	comb.append(com[player])
	qb.append(QB[player])
	total.append(avBP[player]+con[player]+com[player]+QB[player])

df = {
	'Player':players,
	'Avrg BP':abp,
	'Avrg BP/O':abpo,
	'SD':std,
	'Consistency':cons,
	'Combination':comb,
	'QualityB':qb,
	'Total Reselt':total
}

#data = pd.DataFrame(df, index = players)

#data.to_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\FinalFiles\\BowlerFitness.csv',index=players)

