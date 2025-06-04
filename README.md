# FastAPI Job Scraper

This project provides a simple FastAPI application that aggregates remote job postings from several sites.

## Setup

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the server

Start the API with `uvicorn`:

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

## Endpoints

- `GET /` – Health check endpoint returning a basic status message.
- `GET /api/jobs` – Fetches jobs from multiple job boards and returns a JSON list.

