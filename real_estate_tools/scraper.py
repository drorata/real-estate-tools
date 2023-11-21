import requests
from bs4 import BeautifulSoup
from loguru import logger
from typing import List

def getOnlyHREF(linkWithShit):
    return linkWithShit.get('href')

def scrape(url: str) -> List[str]:

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
          'referer':'https://www.zillow.com/homes/Missoula,-MT_rb/'}

    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        #manage-rentals > a > span

        # Find all the article titles on the page
        selector: str = '#grid-search-results > ul > li'
        # selector: str = '#grid-search-results > ul > li > div > div > article > div > div:nth-of-type(2) > div:nth-of-type(2) > a'
        
        linksWithShitFuck = soup.select(selector)

        print(f"size of linksWithShit {len(linksWithShitFuck)}")

        # Using map to get only href
        links = list(map(getOnlyHREF, linksWithShitFuck))
        print(f"size of links {len(links)}")

        print("\nThis shit is:\n")
        print(links)
        # Print the titles
        for link in links:
            print(link)
            print("\n")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")