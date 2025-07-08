import requests
import os
from dotenv import load_dotenv
from nexus.nexus_base.action_manager import agent_action

load_dotenv()

@agent_action
def get_news(query: str = "latest") -> str:
    """Get latest news headlines or search for specific news topics."""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return "❌ Error: NEWS_API_KEY not found in environment variables"
    
    base_url = "https://newsapi.org/v2/top-headlines"
    
    try:
        params = {
            'apiKey': api_key,
            'country': 'us',
            'pageSize': 5
        }
        
        if query != "latest":
            params['q'] = query
            
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data['status'] != 'ok':
            return f"❌ News API error: {data.get('message', 'Unknown error')}"
        
        articles = data['articles']
        if not articles:
            return "📰 No news articles found for your query."
        
        news_summary = "📰 Latest News Headlines:\n\n"
        for i, article in enumerate(articles[:5], 1):
            title = article['title']
            source = article['source']['name']
            description = article.get('description', 'No description available')[:100]
            news_summary += f"{i}. **{title}**\n   Source: {source}\n   {description}...\n\n"
        
        return news_summary.strip()
        
    except Exception as e:
        return f"❌ Error fetching news data: {str(e)}"

