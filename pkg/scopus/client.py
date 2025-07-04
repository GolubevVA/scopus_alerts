from datetime import datetime, timedelta
import aiohttp
from aiolimiter import AsyncLimiter
from .config import MAX_RESULTS_PER_BATCH, MAX_SEARCH_RPS, SEARCH_BASE_URL, LINGUISTICS_ASJC_CODES
from .models import Article

class ScopusClient:
    '''
    Scopus API Client for searching articles.

    Do not forget to call `close()` method when the client is no longer needed to release the aiohttp session.
    '''
    def __init__(self, api_key: str, asjc_codes: list[int] = LINGUISTICS_ASJC_CODES):
        self.api_key = api_key
        self.base_url = SEARCH_BASE_URL
        self.batch_size = MAX_RESULTS_PER_BATCH
        self.headers = {
            'X-ELS-APIKey': self.api_key,
            'Accept': 'application/json'
        }
        self.asjc_codes = asjc_codes

        self.rate_limiter = AsyncLimiter(MAX_SEARCH_RPS, 1)
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession(headers=self.headers)
        return self._session

    async def close(self):
        '''
        Closes the aiohttp session. Should be called when the client is no longer needed.
        '''
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def _search_batch(self, query: str, offset: int) -> dict:
        '''
        Searches for a batch of articles and returns the results.
        '''
        resp = {}
        async with self.rate_limiter:
            session = await self._get_session()
            params = {
                'query': query,
                'sort': '-orig-load-date',
                'count': self.batch_size,
                'start': offset
            }
            async with session.get(self.base_url, params=params) as response:
                resp = await response.json()
        return resp

    async def _get_search_results_count(self, query: str) -> int:
        '''
        Returns the total number of articles that match the query.
        '''
        data = {}
        async with self.rate_limiter:
            session = await self._get_session()
            params = {
                'query': query,
                'count': self.batch_size
            }
            async with session.get(self.base_url, params=params) as response:
                data = await response.json()
    
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
            articles.append(Article.model_validate(entry))
        return articles
    
    async def search(self, date_from: datetime, date_to: datetime) -> list[Article]:
        '''
        All self.asjc_codes subjects related articles from date_from to date_to inclusive.

        Returns a list of articles. Raises an exception if the response is invalid.
        '''
        date_from = date_from - timedelta(days=1)
        date_to = date_to + timedelta(days=1)
        subjects_condition = ' OR '.join([f'SUBJMAIN({subject_id})' for subject_id in self.asjc_codes])
        query = f'ORIG-LOAD-DATE AFT {date_from.strftime("%Y%m%d")} AND ORIG-LOAD-DATE BEF {date_to.strftime("%Y%m%d")} AND ({subjects_condition})'
        total_results = await self._get_search_results_count(query)

        articles: list[Article] = []
        
        for i in range(0, total_results, MAX_RESULTS_PER_BATCH):
            batch_data = await self._search_batch(query, i)
            batch_articles = self._process_search_batch_results(batch_data)
            articles.extend(batch_articles)
        return articles
    
    async def search_by_date(self, date: datetime) -> list[Article]:
        '''
        All self.asjc_codes subjects related articles from the date.

        Returns a list of articles. Raises an exception if the response is invalid.
        '''
        return await self.search(date, date)
