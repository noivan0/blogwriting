from gnews import GNews
from config import GNEWS_MAX_RESULTS

def get_news(keyword: str, period: str = '7d', country: str = 'KR') -> list:
    """
    Fetches news articles for a given keyword using GNews.

    Args:
        keyword (str): The keyword to search for.
        period (str): The time period for the news (e.g., '7d', '1h').
        country (str): The country for the news (e.g., 'US', 'KR').

    Returns:
        list: A list of news article dictionaries, or an empty list if no news is found.
    """
    try:
        print(f"Fetching news for keyword: '{keyword}'...")
        gnews = GNews(language='ko', country=country, period=period, max_results=GNEWS_MAX_RESULTS)
        news = gnews.get_news(keyword)
        
        if not news:
            print(f"No news found for keyword: '{keyword}'")
            return []
            
        print(f"Found {len(news)} articles.")
        return news
    except Exception as e:
        print(f"An error occurred while fetching news: {e}")
        return []
