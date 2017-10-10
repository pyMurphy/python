import requests
from bs4 import BeautifulSoup as bs

header = {'User-Agent': 'Mozilla/5.0'}
heroes = ['ana','bastion','dva','doomfist','genji','hanzo','junkrat','lucio','mccree','mei','mercy','orisa','pharah','reaper','reinhardt','roadhog','soldier76','sombra','symmetra','torbjorn','tracer','widowmaker','winston','zarya','zenyatta']
default_stats = ['eliminations, obj kills, obj time, damage, deaths, weapon acc, critical hits, final blows, solo kills']
available_stats = ', '.join(default_stats)

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

def percentToNumber(percentage):
	percentage = percentage.replace('%','')
	return int(percentage)

def formatNumber(num):
	if ',' in num:
		return num.replace(',','')
	return num

def topRanking(rank):
	if '%' in rank:
		rank = percentToNumber(rank)
		return 100-rank
	return 0

def formatBattletag(battletag):
	if '#' in battletag:
		return ('https://www.overbuff.com/players/pc/'+battletag.replace('#','-'))

def getStat(battletag, stat, hero):
	try:
		if not hero in listHeroes():
			return 'Hero not found.'
		if not stat in listStats(battletag, hero):
			return 'Stat not found.'
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

def getHighestStat(battletag, stat):
	try:
		if not stat in available_stats:
			return 'Stat not found.'
		stats={}
		max_stat=None
		max_hero=None
		for hero in heroes:
			r = requests.get(formatBattletag(battletag)+'/heroes/'+hero, headers=header)
			src = bs(r.text, 'html.parser')
			for div in src.findAll('div',{'class':'stat boxed'}):
				for label in div.findAll('div', {'class':'label'}):
					if label.text.lower() == stat.lower():
						for v in div.findAll('div',{'class':'value'}): 
							value = v.text.strip()
							if '%' in value:
								stats[percentToNumber(value)] = hero
							else:
								stats[float(formatNumber(value))] = hero
		max_stat=list(stats.keys())[0]
		max_hero=stats[max_stat]
		for statistic in stats:
			if statistic > max_stat:
				max_stat=statistic
				max_hero=stats[statistic]
		return ('Highest '+stat+' is '+str(max_stat)+' on '+max_hero)
	except:
		return 'Encountered an error'

def getHeroRanking(battletag, hero, comp=False):
	if not hero in listHeroes():
			return 'Hero not found.'
	if not comp:
		r = requests.get(formatBattletag(battletag)+'/heroes/'+hero, headers=header)
	else:
		r = requests.get(formatBattletag(battletag)+'/heroes/'+hero+'?mode=competitive', headers=header)
	src = bs(r.text, 'html.parser')
	for div in src.findAll('div',{'class':'stat'}):
		for label in div.findAll('div',{'class':'label'}):
			for v in div.findAll('div',{'class':'value'}): 
				top = topRanking(v.text)
				if top != 0:
					return ('Top '+str(top)+'%')
				else:
					return 'Unranked'
	return 'None'

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