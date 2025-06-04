from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import pytest

import main

client = TestClient(main.app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Job scraper API is live!"}


@pytest.mark.asyncio
async def test_get_jobs(monkeypatch):
    async def fake_get(url, headers=None):
        class Response:
            def __init__(self, text):
                self.text = text
        # Return minimal HTML depending on URL
        if "weworkremotely" in url:
            return Response('<section class="jobs"><article><ul><li><a href="/job/1"></a><span class="company">ABC</span><span class="title">Dev</span></li></ul></article></section>')
        elif "jobspresso" in url:
            return Response('<ul class="jobs"><li><a class="job-title" href="/job/2">DevOps</a><div class="job-company">XYZ</div></li></ul>')
        else:
            return Response('<div class="job_listing"><a href="/job/3"></a><div class="job-company">123</div><h3>Engineer</h3></div>')

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def get(self, url, headers=None):
            return await fake_get(url, headers)

    monkeypatch.setattr(main.httpx, "AsyncClient", lambda: FakeClient())

    response = client.get("/api/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "jobs" in data
    assert len(data["jobs"]) == 3

