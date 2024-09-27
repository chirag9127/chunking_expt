import asyncio
import aiohttp
from bs4 import BeautifulSoup
import random

import json
import os

class NotionHelpScraper:
    def __init__(self):
        self.base_url = "https://www.notion.so/help"
        self.articles = []
        self.queue = asyncio.Queue()
        self.visited = set()
        self.checkpoint_file = "checkpoint.json"
        self.raw_pages_dir = "raw_pages"

    async def scrape_notion_help(self):
        self.load_checkpoint()
        await self.queue.put(self.base_url)

        async with aiohttp.ClientSession() as session:
            while not self.queue.empty():
                current_url = await self.queue.get()
                if current_url in self.visited:
                    continue
                
                article_links = await self.extract_article_links(session, current_url)
                
                for link in article_links:
                    if link not in self.visited:
                        await self.queue.put(link)
                
                article_content = await self.scrape_article_content(session, current_url)
                if article_content:
                    self.articles.append(article_content)

                self.visited.add(current_url)
                self.save_checkpoint()
                # Be polite to the server
                await asyncio.sleep(random.uniform(1, 3))

        return self.articles

    async def extract_article_links(self, session, url):
        async with session.get(url) as response:
            content = await response.text()
            self.save_raw_page(url, content)
            soup = BeautifulSoup(content, 'html.parser')
            return [f"https://www.notion.so{link['href']}" for link in soup.select('a[href^="/help/"]')]

    async def scrape_article_content(self, session, article_url):
        raw_content = self.load_raw_page(article_url)
        if raw_content is None:
            async with session.get(article_url) as response:
                raw_content = await response.text()
                self.save_raw_page(article_url, raw_content)
        
        article_soup = BeautifulSoup(raw_content, 'html.parser')
        main_content = article_soup.find('main')
        if main_content:
            for unwanted in main_content.select('nav, .comments, .sidebar'):
                unwanted.extract()
            
            return {
                'url': article_url,
                'title': article_soup.title.string if article_soup.title else '',
                'content': main_content.get_text(strip=True)
            }
        return None

    def load_checkpoint(self):
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)
                self.visited = set(checkpoint_data['visited'])
                self.articles = checkpoint_data['articles']

    def save_checkpoint(self):
        checkpoint_data = {
            'visited': list(self.visited),
            'articles': self.articles
        }
        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint_data, f)

    def save_raw_page(self, url, content):
        if not os.path.exists(self.raw_pages_dir):
            os.makedirs(self.raw_pages_dir)
        filename = os.path.join(self.raw_pages_dir, f"{hash(url)}.html")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

    def load_raw_page(self, url):
        filename = os.path.join(self.raw_pages_dir, f"{hash(url)}.html")
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        return None

if __name__ == "__main__":
    scraper = NotionHelpScraper()
    help_articles = asyncio.run(scraper.scrape_notion_help())
    print(f"Scraped {len(help_articles)} articles from Notion Help Center")
    scraper.load_articles_from_checkpoint()
