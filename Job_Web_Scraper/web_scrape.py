import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import re

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
    url = f'https://ca.indeed.com/jobs?q=intern&l=Toronto%2C+ON&start={page}'
    r = requests.get(url,headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all("div", class_ = 'jobsearch-SerpJobCard')

    for item in divs:
        title = item.find('a').text.strip()
        company = item.find('span',class_ = 'company').text.strip()

        try:
            salary = item.find('span', class_ = 'salaryText').text.strip()
        except:
            salary = ''

        summary = item.find('div', {'class': 'summary'}).text.strip().replace('\n', '')

        job = {
            'Title': title,
            'Company': company,
            'Salary': salary,
            'Summary': summary,
        }
        jobList.append(job)
    return

jobList = []

for i in range(0,40,10):
    print(f'Getting page, {i}')
    c = extract(0)
    transform(c)

df = pd.DataFrame(jobList)

print(df.head())

df.to_csv('jobs.csv')
