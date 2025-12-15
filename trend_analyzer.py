import pandas as pd
from pytrends.request import TrendReq
from config import PYTRENDS_HL, PYTRENDS_GEO

def get_related_keywords(keyword: str) -> list:
    """
    Gets related and trending keywords from Google Trends.

    Args:
        keyword (str): The base keyword to search for.

    Returns:
        list: A list of related keyword strings. Returns an empty list on error.
    """
    try:
        print(f"Finding related keywords for: '{keyword}'...")
        pytrends = TrendReq(hl=PYTRENDS_HL, tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe='today 1-m', geo=PYTRENDS_GEO, gprop='')
        
        related_queries = pytrends.related_queries()
        
        top_keywords = []
        if related_queries.get(keyword) and 'top' in related_queries[keyword] and not related_queries[keyword]['top'].empty:
            top_keywords = related_queries[keyword]['top']['query'].tolist()

        rising_keywords = []
        if related_queries.get(keyword) and 'rising' in related_queries[keyword] and not related_queries[keyword]['rising'].empty:
            rising_keywords = related_queries[keyword]['rising']['query'].tolist()

        # Combine and deduplicate
        all_keywords = list(dict.fromkeys(top_keywords + rising_keywords))
        
        print(f"Found {len(all_keywords)} related keywords.")
        return all_keywords

    except Exception as e:
        print(f"An error occurred while fetching trends: {e}")
        # Pytrends can be flaky and sometimes returns weird errors or empty dataframes
        return []

def select_hot_topic(news_articles: list) -> dict | None:
    """
    Selects the 'hottest' topic from a list of news articles.
    For now, we use a simple heuristic: return the first article.
    This can be expanded later to be more sophisticated.

    Args:
        news_articles (list): A list of news articles from GNews.

    Returns:
        dict | None: The selected article dictionary, or None if the list is empty.
    """
    if not news_articles:
        return None
    
    print(f"Selected article: '{news_articles[0]['title']}'")
    return news_articles[0]
