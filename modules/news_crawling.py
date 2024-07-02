# modules/news_crawling.py

from datetime import datetime, timedelta
import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
import nest_asyncio

nest_asyncio.apply()

async def fetch(session, url, retries=3):
    for attempt in range(retries):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=3000)) as response:
                return await response.text()
        except asyncio.TimeoutError:
            print(f"Timeout error for URL: {url}")
        except aiohttp.ClientError as e:
            print(f"Client error: {e} for URL: {url}")
        except ConnectionResetError:
            print(f"Connection reset error for URL: {url}")
        if attempt < retries - 1:
            await asyncio.sleep(2 ** attempt)  # 지수 백오프
    return None

async def get_news_links(session, base_url, page):
    url = f"{base_url}&page={page}"
    response_text = await fetch(session, url)
    if response_text is None:
        return []
    soup = BeautifulSoup(response_text, 'html.parser')

    links = []
    for a in soup.select("ul.type06_headline li dl dt a"):
        links.append(a["href"])
    for a in soup.select("ul.type06 li dl dt a"):
        links.append(a["href"])

    return links

async def get_news_content(session, url):
    response_text = await fetch(session, url)
    if response_text is None:
        return None, None
    soup = BeautifulSoup(response_text, 'html.parser')

    title_tag = soup.select_one("h2.media_end_head_headline")
    content_tag = soup.find('article', {'id': 'dic_area'})

    if title_tag and content_tag:
        title = title_tag.get_text().strip()
        content = content_tag.get_text().strip()
        return title, content
    return None, None

def scrape_news():
    today = datetime.today().strftime("%Y%m%d")
    base_url = "https://news.naver.com/main/list.naver?mode=LSD&mid=shm&sid1=101&date=" + today

    async def _scrape_news():
        async with aiohttp.ClientSession() as session:
            news_links = set()
            page = 1
            
            while True:
                links = await get_news_links(session, base_url, page)
                if not links or page == 500:
                    break            
                news_links.update(links)
                page += 1

            tasks = [get_news_content(session, link) for link in news_links]
            news_contents = await asyncio.gather(*tasks)

            # None 값을 제거
            news_contents = [content for content in news_contents if content[0] is not None]

            # 명사 추출
            nouns_data = []
            for title, content in news_contents:
                nouns_data.append({'Title': title, 'content': content})

            df = pd.DataFrame(nouns_data)
            df.to_csv(f"/home/hadoop/project/third_project/data/{today}.csv", index=False, encoding='utf-8-sig')

    asyncio.run(_scrape_news())


