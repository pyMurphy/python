# Python Lyrics Finder
#
# DATE	- 04/10/2017
# USER 	- pyMurphy
#
# Small program that returns the lyrics of
# a song using the song title and artist
# through requests to azlyrics.com (don't sue me)

import requests, os
from bs4 import BeautifulSoup
# from colorama import Style, Fore, init
# init(autoreset=True)

# Default user-agent
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# Used to format the string so it can be used in the search
def format_string(s):
	try:
		s = s.lower()		# converts string to lowercase
	except:
		pass
	s = s.replace(' ','+')	# replaces all space characters with '+'
	return s 				# returns new formatted string

# Used to return the text content in the <div> tag the text is stored in
def return_raw_lyrics(name, url):
	elements=[]										# initialise empty elements array
	req = requests.get(url, headers=header)			# request to url
	page = BeautifulSoup(req.text, 'html.parser')	# use beautifulsoup on the page source
	for div in page.findAll('div'):					# find all <div> tags and iterate through them
		elements.append(div.text)					# add text in each <div> tag to the elements array
	for s in elements:								# iterate through the array of text
		if '"'+name+'"' in s.lower():				# check if the text "TITLE" is in the div tag
			return s.lstrip()						# return the text from this div tag and remove leading whitespace

# Returns a cleaned up version of the raw lyrics
def return_lyrics(s,a):
	n = s.find('if  (')								# find the position of text under the lyrics
	lyrics = s[:n].lstrip()							# cut off the rest of the text after the lyrics
	searchterm = (a+' lyrics')						
	n1 = lyrics.lower().find(searchterm)			# search for 'ARTIST lyrics'
	lyrics = lyrics[n1+len(searchterm):].lstrip()	# cut off this text and everything before it
	return lyrics 									# returns actual lyrics

# Returns the lyrics from the song title and artist
def get_lyrics(name, artist):
	results=[]									# initialise empty array for results
	fname = format_string(name) 				# formats the name of the song so it can be used in url search
	r = requests.get('https://search.azlyrics.com/search.php?q='+fname, headers=header)
	page = BeautifulSoup(r.text, 'html.parser')
	for element in page.findAll('td', {'class':'text-left visitedlyr'}):	
		if artist in element.text.lower():		# search for the artist's name in each result
			for link in element.findAll('a'):	# find the link to the lyrics
				results.append(link.get('href'))# return the link
	if len(results) > 1:						# If there are multiple links then we'll make the user choose one
		print('\nMultiple lyrics, choose from links below:\n')
		for i,option in enumerate(results):		# loop through each link
			print(str(i+1)+' - '+option)		# print out like '1 - https://link.com'
		choice = input('\nEnter number: ')		# get user's choice
		try:									# if user entered a valid number then
			results=results[int(choice)-1]		# set results to the link
		except:									# if the number was not valid then
			print('\nInvalid choice, the first link has been chosen by default\n')
			results=results[0]					# set results to the first link
	else:
		try:									# if there is only one link then
			results=results[0]					# set results to only link
		except:
			return 'No results found\n\n\n'
	rawl = return_raw_lyrics(name, results)		# get the raw lyrics
	return return_lyrics(rawl,artist)			# returns the formatted lyrics

def main():
	n = input('Name of song: ')					# gets song name
	a = input('Artist: ')						# gets artist name
	print('\n------------------------------------')
	print('\n'+get_lyrics(n,a))					# prints lyrics
	main()										# starts over

if __name__ == '__main__': 
	os.system('cls')
	main()