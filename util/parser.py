# <Parser file
# by sid 11/4

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

    # store results in a dictionary
    results = []
    
    for item in soup.select('[data-lid]'):
        try:
            add = {}

           # title
            add['title'] = item.select('h3')[0].get_text()

            # PDF url
            add['url'] = item.select('a')[0]['href']

            # citations
            add['citations'] = item.select('.gs_fl')[1].select('a')[2].get_text()

            # TODO: year
            add['date'] = 2016


            # authors
            authors = []
            for i in range(0, len(d[0].find_all('a'))):
                authors.append( d[0].find_all('a')[i].get_text() )

            add['authors'] = ', '.join(authors)
            
            results.append(add)

        except Exception as e:
            # TODO: if we run into an exception, then notify the client
            print(e)
            print("bruh")

    # return a dictionary 
    return results


