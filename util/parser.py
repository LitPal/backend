from bs4 import BeautifulSoup
import requests


# define headers argument
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

# post a request to Google scholar with aour given headers
def post(query: str) -> str:
    # format the google scholar article link
    # 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=web+scraping&btnG='
    base = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q='
    end = '&btnG='

    return requests.get(base + '+'.join(query.split()) + end,headers=headers)


# obtain a google scholar
    # returns a dictionary that contains
def obtainContents(query: str):
    # obtain a post request
    response= post(query)

    # soup query
    soup=BeautifulSoup(response.content, "html.parser") # 'lxml')

    results = []
    
    for item in soup.select('[data-lid]'):
        try:
            add = []

            # title
            add['title'] = item.select('h3')[0].get_text()

            # URL download
            add['url'] = item.select('a')[0]['href']
            
            # text content
            add['content'] = item.select('.gs_rs')[0].get_text()
            
            results.append(add)

        except Exception as e:
            # TODO: if we run into an exception, then notify the client
            print("bruh")

    # return a dictionary 
    return results