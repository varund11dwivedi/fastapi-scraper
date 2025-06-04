from fastapi import FastAPI
\codex/find-issues-and-propose-fixes
import httpx
\main
from bs4 import BeautifulSoup
from typing import List, Dict
import httpx

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Job scraper API is live!"}

@app.get("/api/jobs")
async def get_jobs():
    jobs: List[Dict] = []

    async with httpx.AsyncClient() as client:
        # 1. We Work Remotely
        try:
            wwr_response = await client.get(
                "https://weworkremotely.com/remote-jobs",
                headers={"User-Agent": "Mozilla/5.0"},
            )
            wwr_soup = BeautifulSoup(wwr_response.text, "html.parser")
            sections = wwr_soup.select("section.jobs > article ul li")

            for job in sections:
                link = job.find("a", href=True)
                if link:
                    job_url = "https://weworkremotely.com" + link["href"]
                    company = (
                        job.find("span", class_="company").text.strip()
                        if job.find("span", class_="company")
                        else ""
                    )
                    position = (
                        job.find("span", class_="title").text.strip()
                        if job.find("span", class_="title")
                        else ""
                    )
                    jobs.append(
                        {
                            "source": "We Work Remotely",
                            "company": company,
                            "position": position,
                            "job_link": job_url,
                        }
                    )
        except Exception as e:
            jobs.append({"source": "We Work Remotely", "error": str(e)})

        # 2. Jobspresso
        try:
            jsp_response = await client.get(
                "https://jobspresso.co/remote-developer-jobs/",
                headers={"User-Agent": "Mozilla/5.0"},
            )
            jsp_soup = BeautifulSoup(jsp_response.text, "html.parser")
            posts = jsp_soup.select("ul.jobs li")

            for post in posts:
                title_tag = post.find("a", class_="job-title")
                if title_tag:
                    job_url = title_tag["href"]
                    position = title_tag.get_text(strip=True)
                    company_tag = post.find("div", class_="job-company")
                    company = (
                        company_tag.get_text(strip=True) if company_tag else ""
                    )
                    jobs.append(
                        {
                            "source": "Jobspresso",
                            "company": company,
                            "position": position,
                            "job_link": job_url,
                        }
                    )
        except Exception as e:
            jobs.append({"source": "Jobspresso", "error": str(e)})

        # 3. SkipTheDrive
        try:
            std_response = await client.get(
                "https://www.skipthedrive.com/remote-software-development-jobs/",
                headers={"User-Agent": "Mozilla/5.0"},
            )
            std_soup = BeautifulSoup(std_response.text, "html.parser")
            rows = std_soup.select("div.job_listing")

            for row in rows:
                title = row.select_one("h3")
                company = row.select_one(".job-company")
                job_link_tag = row.select_one("a")

                if job_link_tag:
                    jobs.append(
                        {
                            "source": "SkipTheDrive",
\codex/find-issues-and-propose-fixes
                            "company": company.get_text(strip=True) if company else "",
\
                            "company": company.get_text(strip=True)
                            if company
                            else "",
\main
                            "position": title.get_text(strip=True) if title else "",
                            "job_link": job_link_tag["href"],
                        }
                    )
        except Exception as e:
            jobs.append({"source": "SkipTheDrive", "error": str(e)})

    return {"jobs": jobs}
