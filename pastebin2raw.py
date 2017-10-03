import requests, pyperclip

def pastebin2raw(url):
    id = url.split('.com/')[1]
    return "https://pastebin.com/raw/" + id

def get_raw_source(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    if '/raw/' not in url:
    	url = pastebin2raw(url)
    source = requests.get(url, headers=headers)
    return source.text

url_get = input('Enter pastebin URL: ')
raw_code = get_raw_source(url_get)
print(raw_code)
pyperclip.copy(raw_code)
print('\nSource copied to clipboard!')