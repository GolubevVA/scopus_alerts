import pytest
from datetime import datetime
from pkg.scopus import ScopusClient, Article

def test_client_initialization(scopus_api_key: str, scopus_client: ScopusClient):
    assert scopus_client.api_key == scopus_api_key
    assert "X-ELS-APIKey" in scopus_client.headers
    assert scopus_client.headers["Accept"] == "application/json"

@pytest.mark.asyncio
async def test_real_search(scopus_client: ScopusClient):
	"""Test actual search with real API call"""
	date_from = datetime(2025, 5, 21)
	date_to = datetime(2025, 5, 22)
    
	results = await scopus_client.search(date_from, date_to)
    
	assert isinstance(results, list)
    
	assert len(results) > 0
	assert all(isinstance(article, Article) for article in results)
	assert all(len(article.title) > 0 for article in results)

def assert_search_results_eq(results_1: list[Article], results_2: list[Article], fraction_success: float = 0.90):
	"""
	Check if two search results are equal based on titles. 
	
	The fraction of successful matches should be at least `fraction_success`.
	
	The reason for this unstable test is that Scopus API may return different results for the same query.
	"""
	assert len(results_1) == len(results_2)
	assert all(isinstance(article, Article) for article in results_1)
	assert all(len(article.title) > 0 for article in results_1)
	assert all(isinstance(article, Article) for article in results_2)
	assert all(len(article.title) > 0 for article in results_2)

	n = len(results_1)
	success = 0
	
	set_titles_1 = {article.title for article in results_1}
	set_titles_2 = {article.title for article in results_2}
	sets_intersection = set_titles_1.intersection(set_titles_2)
	success = len(sets_intersection)
	
	assert success >= fraction_success * n, f"Only {success} out of {n} articles matched, expected at least {fraction_success * n} matches."

def results_sorted_key(x: Article):
	"""Key function for sorting results"""
	affil_tuple = tuple((aff.name, aff.city, aff.country) for aff in sorted(x.affiliations, key=lambda a: (a.name, a.city, a.country)))
	return (x.scopus_link, x.title, x.publication_name, x.creator, affil_tuple)

@pytest.mark.asyncio
async def test_real_search_by_date(scopus_client: ScopusClient):
	"""Test search_by_date with real API call"""
	target_date = datetime(2025, 5, 22)
    
	results = await scopus_client.search_by_date(target_date)
	results = sorted(results, key=results_sorted_key)
    
	results_same = await scopus_client.search(target_date, target_date)
	results_same = sorted(results_same, key=results_sorted_key)
    
	assert len(results) == len(results_same)
	assert all(isinstance(article, Article) for article in results)
	assert all(len(article.title) > 0 for article in results)
	
	assert_search_results_eq(results, results_same)

@pytest.mark.asyncio
async def test_extracts_exactly_one_day(scopus_client: ScopusClient):
	""""This test checks that the search_by_date function's results joined with the sequential day are the same as just search for the same days"""
	target_date_1 = datetime(2025, 5, 21)
	target_date_2 = datetime(2025, 5, 22)
	
	results_1 = await scopus_client.search_by_date(target_date_1)
	results_2 = await scopus_client.search_by_date(target_date_2)
	assert len(results_1) > 0
	assert len(results_2) > 0
	results = sorted((results_2 + results_1), key=results_sorted_key)
	results_same = sorted(await scopus_client.search(target_date_1, target_date_2), key=results_sorted_key)
	
	assert len(results) == len(results_same)
	assert all(isinstance(article, Article) for article in results)
	assert all(len(article.title) > 0 for article in results)
	
	assert_search_results_eq(results, results_same)
