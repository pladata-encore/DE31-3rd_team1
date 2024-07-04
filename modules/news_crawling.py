from datetime import datetime
import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
import nest_asyncio
import os
import subprocess
from pyarrow import fs
import pyarrow as pa
import pyarrow.csv as pc

# nest_asyncio는 기존 asyncio 이벤트 루프를 중첩할 수 있게 해줍니다.
nest_asyncio.apply()

# 웹 페이지에서 데이터를 비동기로 가져오는 함수
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

# 뉴스 링크를 가져오는 함수
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

# 뉴스 내용을 가져오는 함수
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

# 뉴스 스크래핑 함수
def scrape_news():
    # 오늘 날짜를 기반으로 뉴스 URL 설정
    news_today = datetime.today().strftime("%Y%m%d")
    base_url = "https://news.naver.com/main/list.naver?mode=LSD&mid=shm&sid1=101&date=" + news_today

    async def _scrape_news():
        async with aiohttp.ClientSession() as session:
            news_links = set()
            page = 1
            
            while True:
                links = await get_news_links(session, base_url, page)
                if not links or page == 500:
                    print("링크 다 불러왔어요!")
                    break            
                news_links.update(links)
                page += 1

            tasks = [get_news_content(session, link) for link in news_links]
            news_contents = await asyncio.gather(*tasks)

            # None 값을 제거
            news_contents = [content for content in news_contents if content[0] is not None]

            # 뉴스 데이터를 명사로 추출하여 DataFrame에 저장
            nouns_data = []
            for title, content in news_contents:
                nouns_data.append({'Title': title, 'content': content})

            df = pd.DataFrame(nouns_data)
            # DataFrame을 JSON 문자열로 변환하여 리턴
            return df.to_json(orient='records')

    return asyncio.run(_scrape_news())

# JSON 데이터를 HDFS로 전송하는 함수
def transfer_to_hdfs(json_data):
    today = datetime.today().strftime("%Y-%m-%d")
    file_path = f"/test/{today}.csv"
    # Hadoop classpath 설정
    classpath = subprocess.Popen(["/home/ksk/hadoop/bin/hdfs", "classpath", "--glob"], stdout=subprocess.PIPE).communicate()[0]
    os.environ["CLASSPATH"] = classpath.decode("utf-8")
    hdfs = fs.HadoopFileSystem(host='192.168.0.206', port=8020, user='ksk')

    # JSON 데이터를 DataFrame으로 변환
    df = pd.read_json(json_data, orient='records')

    # Pandas DataFrame을 PyArrow의 Table 객체로 변환
    table = pa.Table.from_pandas(df)
    
    # HDFS에 Parquet 파일로 저장
    with hdfs.open_output_stream(file_path) as stream:
        pc.write_csv(table, stream)
    print(f"DataFrame saved to HDFS at {file_path}")
