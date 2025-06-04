from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/scrape-jobs")
def scrape_jobs():
    url = 'https://remoteok.com/remote-dev-jobs'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    job_rows = soup.find_all('tr', class_='job')

    for job in job_rows:
        try:
            company = job.find('h3').text.strip()
            title = job.find('h2').text.strip()
            link = 'https://remoteok.com' + job['data-href']
            jobs.append({
                'company': company,
                'title': title,
                'link': link
            })
        except:
            continue

    return jobs
