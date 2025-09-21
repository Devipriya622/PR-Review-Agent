# src/fetchers/github_fetcher.py
import requests
from src.config import Config
from .base_fetcher import BaseFetcher

class GitHubFetcher(BaseFetcher):
    BASE = "https://api.github.com"
    def __init__(self, token: str = None):
        self.token = token or Config.GITHUB_TOKEN
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({"Authorization": f"token {self.token}"})
        self.session.headers.update({"Accept": "application/vnd.github.v3+json"})
    def fetch_pr(self, repo: str, pr_id: str):
        pr_url = f"{self.BASE}/repos/{repo}/pulls/{pr_id}"
        r = self.session.get(pr_url, timeout=Config.REQUEST_TIMEOUT)
        r.raise_for_status()
        pr = r.json()
        files_url = pr_url + "/files"
        files, page = [], 1
        while True:
            r2 = self.session.get(files_url, params={"page": page, "per_page": 100}, timeout=Config.REQUEST_TIMEOUT)
            r2.raise_for_status()
            batch = r2.json()
            if not batch:
                break
            for f in batch:
                files.append({
                    "filename": f.get("filename"),
                    "patch": f.get("patch") or "",
                    "raw_url": f.get("raw_url"),
                    "status": f.get("status")
                })
            page += 1
        return {
            "title": pr.get("title"),
            "author": pr.get("user", {}).get("login"),
            "body": pr.get("body"),
            "files": files,
            "url": pr.get("html_url")
        }
