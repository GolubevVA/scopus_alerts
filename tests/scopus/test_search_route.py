import pytest
from datetime import datetime
from pkg.scopus.client import ScopusClient
from pkg.scopus.models import Article, Affilation

def test_client_initialization(scopus_api_key, scopus_client: ScopusClient):
    assert scopus_client.api_key == scopus_api_key
    assert "X-ELS-APIKey" in scopus_client.headers
    assert scopus_client.headers["Accept"] == "application/json"

def test_real_search(scopus_client: ScopusClient):
	"""Test actual search with real API call"""
	date_from = datetime(2025, 5, 21)
	date_to = datetime(2025, 5, 22)
    
	results = scopus_client.search(date_from, date_to)
    
	assert isinstance(results, list)
    
	assert len(results) > 0
	assert all(isinstance(article, Article) for article in results)
	assert all(len(article.title) > 0 for article in results)

def assert_search_results_eq(results_1, results_2):
	"""Check if two search results are equal"""
	assert len(results_1) == len(results_2)
	assert all(isinstance(article, Article) for article in results_1)
	assert all(len(article.title) > 0 for article in results_1)
	
	for i in range(len(results_1)):
		assert results_1[i].title == results_2[i].title
		assert results_1[i].publication_name == results_2[i].publication_name
		assert results_1[i].scopus_link == results_2[i].scopus_link
		assert results_1[i].creator == results_2[i].creator
		assert len(results_1[i].affiliations) == len(results_2[i].affiliations)
		for j in range(len(results_1[i].affiliations)):
			assert results_1[i].affiliations[j].name == results_2[i].affiliations[j].name
			assert results_1[i].affiliations[j].city == results_2[i].affiliations[j].city
			assert results_1[i].affiliations[j].country == results_2[i].affiliations[j].country

def test_real_search_by_date(scopus_client: ScopusClient):
	"""Test search_by_date with real API call"""
	target_date = datetime(2025, 5, 22)
    
	results = scopus_client.search_by_date(target_date)
    
	results_same = scopus_client.search(target_date, target_date)
    
	assert len(results) == len(results_same)
	assert all(isinstance(article, Article) for article in results)
	assert all(len(article.title) > 0 for article in results)
	
	assert_search_results_eq(results, results_same)

def test_extracts_exactly_one_day(scopus_client: ScopusClient):
	""""This test checks that the search_by_date function's results joined with the sequential day are the same as just search for the same days"""
	target_date_1 = datetime(2025, 5, 21)
	target_date_2 = datetime(2025, 5, 22)
	
	results_1 = scopus_client.search_by_date(target_date_1)
	results_2 = scopus_client.search_by_date(target_date_2)
	assert len(results_1) > 0
	assert len(results_2) > 0
	results = results_2 + results_1
	results_same = scopus_client.search(target_date_1, target_date_2)
	
	assert len(results) == len(results_same)
	assert all(isinstance(article, Article) for article in results)
	assert all(len(article.title) > 0 for article in results)
	
	assert_search_results_eq(results, results_same)
