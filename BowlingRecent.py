import numpy as np
import pandas as pd 
import random as rn 
import math


inningsDataR = pd.read_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\BangladeshT20BowlingRecent.csv')

#print(inningsDataBP['Start Date'])
players = set(inningsDataR['Player'])

def playerRecentAvrg():
	PlayerSerialBP = {}

	for player in players:
		overs = [ inningsDataR['Overs'][i]  for i in range(len(inningsDataR)) if inningsDataR['Player'][i]==player][::-1]
		runs = [ int(inningsDataR['Runs'][i])  for i in range(len(inningsDataR)) if inningsDataR['Player'][i]==player][::-1]
		wkts = [ int(inningsDataR['Wkts'][i])  for i in range(len(inningsDataR)) if inningsDataR['Player'][i]==player][::-1]
		total = 0
		count = 0
		for i in range(len(overs)):
			o = float(overs[i])
			over = int(o) + (o - int(o))*(10/6)
			run = int(runs[i])
			point = run * (run/(over*6)) + ((20 - (wkts[i]*5)) * (over/4))
			total += point*((.96)**i)
			count += over*((.96)**i)

		PlayerSerialBP[player] = total/count


	return PlayerSerialBP


#print(playerRecentAvrg())

def teamBP(date):
	total = 0
	totalOver = 0
	for i in range(len(inningsDataR)):
		if inningsDataR['Start Date'][i] == date:
			if inningsDataR['Overs'][i] == 'DNB' or inningsDataR['Overs'][i]=='TDNB':
				over = 0
			else:
				o = float(inningsDataR['Overs'][i])
				over = int(o) + (o - int(o))*(10/6)
				totalOver += over
				run = int(inningsDataR['Runs'][i])
	#			print(run)
				total += ((run**2)/(over*6))
	#print(total,totalOver)
	return (total/totalOver)

#print(teamBP('18-Sep-07'))

def qualityBowling():
	QB = []
	for i in range(len(inningsDataR)):
		if inningsDataR['Overs'][i] == 'DNB' or inningsDataR['Overs'][i]=='TDNB':
			QB.append(0)
		else:
			o = float(inningsDataR['Overs'][i])
			over = int(o) + (o - int(o))*(10/6)
			date = inningsDataR['Start Date'][i]
			point = over * ((inningsDataR['BP'][i]/over)-teamBP(date))
			QB.append(point)

	return QB