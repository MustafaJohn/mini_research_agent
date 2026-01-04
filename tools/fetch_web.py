# Code for fetching data from the web
import os
import time
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS  
import hashlib
import re

class FetchWebTool:
    """
    A tool for fetching data from the web using DuckDuckGo search and BeautifulSoup.
    Responsibilities:
      - Search the web for a query
      - Download raw HTML
      - Extract readable text
      - Store raw pages to disk
    """

    def __init__(self, raw_data_dir="data\\raw", rate_limit=1.5):
        self.raw_data_dir = raw_data_dir
        self.rate_limit = rate_limit
        os.makedirs(self.raw_data_dir, exist_ok=True)

    # Function to search on DuckDuckGo
    def search(self, query, n_results=10):
        """Returns a list of URLs from DuckDuckGo search results."""
        with DDGS() as ddgs:
            results = ddgs.text(query, region="uk-en", max_results=n_results)
            urls = [result["href"] for result in results if "href" in result]
        return urls 
    
    # Function to clean the URL
    

    def _clean_url(self, url: str) -> str:

        h = hashlib.md5(url.encode()).hexdigest()[:12]
        base = re.sub(r"[^a-zA-Z0-9_-]", "_", url)
        return f"{base[:50]}_{h}.txt"

    def _already_downloaded(self, url):
        """Check if this URL has already been fetched."""
        filename = self._clean_url(url)
        return os.path.exists(os.path.join(self.raw_data_dir, filename))
    
    def fetch_url(self, url):
        """
        Download + extract readable text + save locally.
        No retries yet
        """
        filename = self._clean_url(url)
        file_path = os.path.join(self.raw_data_dir, filename)
        
        if self._already_downloaded(url):
            #print(f"[cached] {url}")
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        try:
            #print(f"[fetching] {url}")
            response = requests.get(url, timeout=12, headers={
                "User-Agent": "Research Agent"
            })
            response.raise_for_status()
        except Exception as e:
            #print(f"[ERROR] fetching {url}: {e}")
            return ""
            
        soup = BeautifulSoup(response.text, "html.parser")
            
        # Extract readable text 
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()

        text = soup.get_text(separator="\n")
        cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())
            
        # Save to disk in raw data directory as txt file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned)
            
        time.sleep(self.rate_limit)
        return cleaned

    def fetch_query(self, query, n_results=10):
        """ Search + fetch URLs for a given input"""
        urls = self.search(query, n_results=n_results)
        pages = []
        print("\nSources fetched:")
        # Presenting a high level output of urls and their text  
        for url in urls:
            text = self.fetch_url(url)
            if text:
                print(f"- {url}")
            pages.append({'url': url, 'text': text})
        
        return pages

#if __name__ == "__main__":
#    tool = FetchWebTool()
#    data = tool.fetch_query("potato", n_results=2)
#    print(f"Fetched {len(data)} pages.") 