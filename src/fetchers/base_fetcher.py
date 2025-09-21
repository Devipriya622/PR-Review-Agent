# src/fetchers/base_fetcher.py
from abc import ABC, abstractmethod

class BaseFetcher(ABC):
    @abstractmethod
    def fetch_pr(self, repo: str, pr_id: str):
        raise NotImplementedError
