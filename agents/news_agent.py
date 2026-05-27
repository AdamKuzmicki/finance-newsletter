"""
News Agent
----------
Fetches top financial news from NewsAPI.org.

How it works:
- We make HTTP GET requests to the NewsAPI endpoint
- We search for finance/business/market news from the last 24 hours
- We return the top 10 articles with title, description, and source
- Claude then synthesizes these into newsletter summaries

API docs: https://newsapi.org/docs/endpoints/everything
"""

import requests
from datetime import datetime, timedelta
from config.settings import NEWS_API_KEY


# Search queries for different finance topics
NEWS_QUERIES = [
    "stock market Federal Reserve economy",
    "banking finance earnings Wall Street",
    "cryptocurrency bitcoin crypto market",
    "technology AI earnings revenue",
    "geopolitics trade oil sanctions",
]


def fetch_news(query: str, max_articles: int = 5) -> list[dict]:
    """
    Fetch news articles for a given search query.
    
    Returns a list of article dicts with keys:
      title, description, source, url, publishedAt
    """
    # NewsAPI 'everything' endpoint — searches all sources
    url = "https://newsapi.org/v2/everything"
    
    # Yesterday's date for filtering recent news
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    params = {
        "q": query,
        "from": yesterday,
        "sortBy": "relevancy",      # most relevant first
        "language": "en",
        "pageSize": max_articles,
        "apiKey": NEWS_API_KEY,
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # raises exception if HTTP error
        
        data = response.json()
        articles = data.get("articles", [])
        
        # Clean up and return only what we need
        return [
            {
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "source": a.get("source", {}).get("name", "Unknown"),
                "url": a.get("url", ""),
                "published": a.get("publishedAt", ""),
            }
            for a in articles
            if a.get("title") and "[Removed]" not in a.get("title", "")
        ]
    
    except requests.exceptions.RequestException as e:
        print(f"Warning: News fetch failed for '{query}': {e}")
        return []


def get_all_news() -> list[dict]:
    """
    Fetch news across all our topic queries.
    Deduplicates articles by title.
    Returns up to 20 unique articles.
    """
    print("Fetching financial news...")
    
    all_articles = []
    seen_titles = set()
    
    for query in NEWS_QUERIES:
        articles = fetch_news(query, max_articles=4)
        
        for article in articles:
            # Deduplicate: skip if we already have this headline
            title_key = article["title"][:50].lower()
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                all_articles.append(article)
        
        print(f"  ✓ '{query[:30]}...' — {len(articles)} articles")
    
    print(f"  Total unique articles: {len(all_articles)}")
    return all_articles[:20]  # cap at 20


def format_news_for_prompt(articles: list[dict]) -> str:
    """
    Format news articles as a numbered list for Claude's prompt.
    Claude will synthesize these into newsletter-ready summaries.
    """
    if not articles:
        return "No news articles available. Generate market commentary from general knowledge."
    
    lines = ["TOP FINANCIAL NEWS ARTICLES (summarize and analyze these):\n"]
    
    for i, article in enumerate(articles, 1):
        lines.append(f"{i}. [{article['source']}] {article['title']}")
        if article["description"]:
            lines.append(f"   {article['description'][:200]}")
        lines.append("")
    
    return "\n".join(lines)
