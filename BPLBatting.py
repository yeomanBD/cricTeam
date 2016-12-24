import numpy as np
import pandas as pd 
import random as rn 
import math

'''Coding section for loading data'''

bplRecent = pd.read_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\BPLRecentBattingPoints.csv')
bplOveral = pd.read_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\BPLOverallBattingPoints.csv')

playerR = list(bplRecent['Player'])
playerO = list(bplOveral['Player'])
players = set()
for player in playerO:
	players.add(player)
for player in playerR:
	players.add(player)

def o():
	o = {}
	for i in range(len(playerO)):
		o[bplOveral['Player'][i]] = bplOveral['Total Points'][i]

	return o

def r():
	o = {}
	for i in range(len(playerR)):
		o[bplRecent['Player'][i]] = bplRecent['Total Points'][i]

	return o

O = o()
R = r()
overall = []; recent = []; total = [];Players=[]
for player in players:
	Players.append(player)
	if player in set(playerO):
		overall.append(O[player])
		x = O[player]
	else:
		overall.append(0)
		x = 0

	if player in set(playerR):
		recent.append(R[player])
		y = R[player]
	else:
		recent.append(0)
		y = 0
	total.append(x*.333 + y*.666)

d = {
	'Player':Players,
	'overall':overall,
	'recent':recent,
	'Total':total
}

data = pd.DataFrame(d,index = Players)
data.to_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\FinalFiles\\BPLRecent.csv',index=Players)
