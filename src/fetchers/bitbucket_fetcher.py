# src/fetchers/bitbucket_fetcher.py
import requests
from src.config import Config
from .base_fetcher import BaseFetcher

class BitbucketFetcher(BaseFetcher):
    BASE = "https://api.bitbucket.org/2.0"
    def __init__(self, username=None, app_password=None):
        self.username = username or Config.BITBUCKET_USERNAME
        self.app_password = app_password or Config.BITBUCKET_APP_PASSWORD
        self.session = requests.Session()
        if self.username and self.app_password:
            self.session.auth = (self.username, self.app_password)
    def fetch_pr(self, repo: str, pr_id: str):
        pr_url = f"{self.BASE}/repositories/{repo}/pullrequests/{pr_id}"
        r = self.session.get(pr_url, timeout=Config.REQUEST_TIMEOUT)
        r.raise_for_status()
        pr = r.json()
        files = []
        diffstat_url = pr_url + "/diffstat"
        page = 1
        while True:
            r2 = self.session.get(diffstat_url, params={"page": page, "pagelen": 50}, timeout=Config.REQUEST_TIMEOUT)
            r2.raise_for_status()
            data = r2.json()
            for v in data.get("values", []):
                files.append({
                    "filename": v.get("new", {}).get("path") or v.get("old", {}).get("path"),
                    "patch": "",
                    "raw_url": None,
                    "status": v.get("status")
                })
            if not data.get("next"):
                break
            page += 1
        return {
            "title": pr.get("title"),
            "author": pr.get("author", {}).get("nickname"),
            "body": pr.get("description"),
            "files": files,
            "url": pr.get("links", {}).get("html", {}).get("href")
        }
