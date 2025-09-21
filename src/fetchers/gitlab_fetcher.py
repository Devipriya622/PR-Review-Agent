# src/fetchers/gitlab_fetcher.py
import requests
from src.config import Config
from .base_fetcher import BaseFetcher
from urllib.parse import quote_plus

class GitLabFetcher(BaseFetcher):
    def __init__(self, token: str = None, base_url="https://gitlab.com"):
        self.token = token or Config.GITLAB_TOKEN
        self.base = base_url.rstrip("/")
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({"PRIVATE-TOKEN": self.token})
    def fetch_pr(self, repo: str, pr_id: str):
        proj = quote_plus(repo)
        mr_url = f"{self.base}/api/v4/projects/{proj}/merge_requests/{pr_id}"
        r = self.session.get(mr_url, timeout=Config.REQUEST_TIMEOUT)
        r.raise_for_status()
        mr = r.json()
        diffs_url = mr_url + "/changes"
        r2 = self.session.get(diffs_url, timeout=Config.REQUEST_TIMEOUT)
        r2.raise_for_status()
        changes = r2.json().get("changes", [])
        files = []
        for c in changes:
            files.append({
                "filename": c.get("new_path") or c.get("old_path"),
                "patch": c.get("diff") or "",
                "raw_url": None,
                "status": c.get("new_file") and "added" or (c.get("deleted_file") and "removed" or "modified")
            })
        return {
            "title": mr.get("title"),
            "author": mr.get("author", {}).get("username"),
            "body": mr.get("description"),
            "files": files,
            "url": mr.get("web_url")
        }
