import requests
from bs4 import BeautifulSoup as bs

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
heroes = ['ana','bastion','dva','doomfist','genji','hanzo','junkrat','lucio','mccree','mei','mercy','orisa','pharah','reaper','reinhardt','roadhog','soldier76','sombra','symmetra','torbjorn','tracer','widowmaker','winston','zarya','zenyatta']

def getUser(battletag):
	r = requests.get(formatBattletag(battletag), headers=header)
	return bs(r.text, 'html.parser')

def userFound(battletag):
	r = requests.get(formatBattletag(battletag), headers=header)
	if '<h1>Not Found</h1>' in r.text:
		return False
	else:
		return True

def listHeroes():
	return ', '.join(heroes)

def listStats(battletag, hero):
	stats=[]
	r = requests.get(formatBattletag(battletag)+'/heroes/'+hero, headers=header)
	src = bs(r.text, 'html.parser')
	for div in src.findAll('div',{'class':'stat boxed'}):
		for label in div.findAll('div', {'class':'label'}):
			stats.append(label.text.lower())
	return ', '.join(stats)

def formatBattletag(battletag):
	if '#' in battletag:
		return ('https://www.overbuff.com/players/pc/'+battletag.replace('#','-'))

def getStat(battletag, stat, hero):
	try:
		if not hero in listHeroes():
			return 'Hero not found. Here are a list of valid heroes: '+listHeroes()
		if not stat in listStats(battletag, hero):
			return 'Stat not found. Here are a list of valid stats: '+listStats(battletag, hero)
		r = requests.get(formatBattletag(battletag)+'/heroes/'+hero, headers=header)
		src = bs(r.text, 'html.parser')
		for div in src.findAll('div',{'class':'stat boxed'}):
			for label in div.findAll('div', {'class':'label'}):
				if label.text.lower() == stat.lower():
					for v in div.findAll('div',{'class':'value'}): 
						return v.text
		return 'None'
	except:
		return 'Encountered an error'

def compareStats(battletag1, battletag2, stat, hero):
	stat1 = getStat(battletag1, stat, hero)
	stat2 = getStat(battletag2, stat, hero)
	return (battletag1+"'s "+stat+": "+stat1+"\n"+battletag2+"'s "+stat+": "+stat2)

def getLevel(battletag):
	try:
		src = getUser(battletag)
		if not userFound(battletag): return 'User not found'
		for div in src.findAll('div', {'class':'corner corner-text'}):
			return div.text
	except:
		return 'Encountered an error'

def getSR(battletag):
	try:
		src = getUser(battletag)
		if not userFound(battletag): return 'User not found'
		if len(src.findAll('span', {'class': 'color-stat-rating'})) > 0:
			for heading in src.findAll('span', {'class': 'color-stat-rating'}):
				return heading.text
		else:
			return '0'
	except:
		return 'Encountered an error'