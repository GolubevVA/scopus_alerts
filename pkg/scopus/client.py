from datetime import datetime, timedelta
import requests
from urllib.parse import quote
from time import sleep
from time import time
from .config import MAX_RESULTS_PER_BATCH, MAX_SEARCH_RPS, BASE_URL
from .models import Article

class ScopusClient:
    '''
    The client cannot be used asynchronously or concurrently, because it should fit in the rate limits.
    '''
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = BASE_URL
        self.headers = {
            'X-ELS-APIKey': self.api_key,
            'Accept': 'application/json'
        }

    def _search_batch(self, query: str, offset: int) -> dict:
        '''
        Searches for a batch of articles and returns the results.

        Sleeps enough to fit in the rate limits.
        '''
        start_time = time()
        url = f'{self.base_url}?query={quote(query)}&sort=-orig-load-date&count={MAX_RESULTS_PER_BATCH}&start={offset}'
        response = requests.get(url, headers=self.headers)
        data = response.json()
        end_time = time()
        if end_time - start_time < 1. / MAX_SEARCH_RPS:
            sleep(1. / MAX_SEARCH_RPS - (end_time - start_time))
        return data

    def _get_search_results_count(self, query: str) -> int:
        '''
        Returns the total number of articles that match the query.

        Sleeps enough to fit in the rate limits.
        '''
        url = f'{self.base_url}?query={quote(query)}&count={MAX_RESULTS_PER_BATCH}'
        response = requests.get(url, headers=self.headers)
        data = response.json()
        if 'search-results' not in data or 'opensearch:totalResults' not in data['search-results']:
            raise Exception(f'Invalid response: {data}')
        return int(data['search-results']['opensearch:totalResults'])
    
    def _process_search_batch_results(self, data: dict) -> list[Article]:
        '''
        Processes a batch of articles and returns the results.

        Raises an exception if the response is invalid.
        '''
        if 'search-results' not in data or 'entry' not in data['search-results']:
            raise Exception(f'Invalid response: {data}')
        articles: list[Article] = []
        for entry in data['search-results']['entry']:
            articles.append(Article(entry))
        return articles
    
    def search(self, date_from: datetime, date_to: datetime) -> list[Article]:
        '''
        All the linguistics related articles from date_from to date_to inclusive.

        Returns a list of articles. Raises an exception if the response is invalid.
        '''
        date_from = date_from - timedelta(days=1)
        date_to = date_to + timedelta(days=1)
        query = f'ORIG-LOAD-DATE AFT {date_from.strftime("%Y%m%d")} AND ORIG-LOAD-DATE BEF {date_to.strftime("%Y%m%d")} AND (SUBJMAIN(1203) OR SUBJMAIN(3310))'
        total_results = self._get_search_results_count(query)

        articles: list[Article] = []
        
        for i in range(0, total_results, MAX_RESULTS_PER_BATCH):
            batch_data = self._search_batch(query, i)
            batch_articles = self._process_search_batch_results(batch_data)
            articles.extend(batch_articles)
        return articles
    
    def search_by_date(self, date: datetime) -> list[Article]:
        '''
        All the linguistics related articles from the date.

        Returns a list of articles. Raises an exception if the response is invalid.
        '''
        return self.search(date, date)
