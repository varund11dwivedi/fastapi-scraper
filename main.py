from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/api/jobs")
def get_remoteok_jobs():
    url = 'https://remoteok.io/remote-dev-jobs'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch jobs"}

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []

    for job_row in soup.select('tr.job'):
        company = job_row.get('data-company')
        position = job_row.get('data-position') or job_row.get('data-title')
        job_url = 'https://remoteok.io' + job_row.get('data-url') if job_row.get('data-url') else ''
        tags = [tag.text.strip() for tag in job_row.select('.tag')]

        jobs.append({
            "company": company,
            "position": position,
            "job_link": job_url,
            "tags": tags
        })

    return {"jobs": jobs}