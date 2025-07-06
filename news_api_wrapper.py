import asyncio
import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.functions import kernel_function
from semantic_kernel.contents.chat_history import ChatHistory

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

class NewsService:
    """Plugin for fetching news from NewsAPI.org"""
    
    def __init__(self):
        # Get a free API key from https://newsapi.org/
        # Add NEWS_API_KEY=your_key_here to your .env file
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"
    
    @kernel_function(
        description="Gets latest news headlines from various sources",
        name="get_top_headlines"
    )
    def get_top_headlines(self, country: str = "us") -> str:
        """Get top headlines for a country"""
        if not self.news_api_key:
            return "News API key not configured. Please add NEWS_API_KEY to your .env file. Get one free at https://newsapi.org/"
        
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'apiKey': self.news_api_key,
                'country': country,
                'pageSize': 10
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                
                for article in data.get('articles', [])[:5]:  # Limit to 5 articles
                    articles.append({
                        'title': article.get('title', 'No title'),
                        'description': article.get('description', 'No description'),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'url': article.get('url', ''),
                        'publishedAt': article.get('publishedAt', '')
                    })
                
                return json.dumps({'articles': articles, 'totalResults': data.get('totalResults', 0)})
            else:
                return f"Error fetching news: {response.status_code}"
                
        except Exception as e:
            return f"Error getting news: {str(e)}"
    
    @kernel_function(
        description="Searches for news articles about a specific topic",
        name="search_news"
    )
    def search_news(self, topic: str) -> str:
        """Search for news articles about a specific topic"""
        if not self.news_api_key:
            return "News API key not configured. Please add NEWS_API_KEY to your .env file."
        
        try:
            url = f"{self.base_url}/everything"
            params = {
                'apiKey': self.news_api_key,
                'q': topic,
                'sortBy': 'publishedAt',
                'pageSize': 5,
                'language': 'en'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                
                for article in data.get('articles', []):
                    articles.append({
                        'title': article.get('title', 'No title'),
                        'description': article.get('description', 'No description'),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'url': article.get('url', ''),
                        'publishedAt': article.get('publishedAt', '')
                    })
                
                return json.dumps({'articles': articles, 'totalResults': data.get('totalResults', 0)})
            else:
                return f"Error searching news for '{topic}': {response.status_code}"
                
        except Exception as e:
            return f"Error searching news: {str(e)}"
    
    @kernel_function(
        description="Gets news from specific sources",
        name="get_news_by_source"
    )
    def get_news_by_source(self, sources: str) -> str:
        """Get news from specific sources (comma-separated)"""
        if not self.news_api_key:
            return "News API key not configured."
        
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'apiKey': self.news_api_key,
                'sources': sources,
                'pageSize': 5
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                
                for article in data.get('articles', []):
                    articles.append({
                        'title': article.get('title', 'No title'),
                        'description': article.get('description', 'No description'),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'url': article.get('url', ''),
                        'publishedAt': article.get('publishedAt', '')
                    })
                
                return json.dumps({'articles': articles, 'totalResults': data.get('totalResults', 0)})
            else:
                return f"Error fetching news from sources '{sources}': {response.status_code}"
                
        except Exception as e:
            return f"Error getting news by source: {str(e)}"
    
    @kernel_function(
        description="Gets available news sources",
        name="get_news_sources"
    )
    def get_news_sources(self, category: str = "") -> str:
        """Get available news sources, optionally filtered by category"""
        if not self.news_api_key:
            return "News API key not configured."
        
        try:
            url = f"{self.base_url}/sources"
            params = {
                'apiKey': self.news_api_key,
                'language': 'en'
            }
            
            if category:
                params['category'] = category
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                sources = []
                
                for source in data.get('sources', [])[:10]:  # Limit to 10 sources
                    sources.append({
                        'id': source.get('id', ''),
                        'name': source.get('name', ''),
                        'description': source.get('description', ''),
                        'category': source.get('category', ''),
                        'country': source.get('country', '')
                    })
                
                return json.dumps({'sources': sources})
            else:
                return f"Error fetching sources: {response.status_code}"
                
        except Exception as e:
            return f"Error getting sources: {str(e)}"
    
    @kernel_function(
        description="Gets news help and available commands",
        name="get_news_help"
    )
    def get_news_help(self) -> str:
        """Get help information about news commands"""
        return """News Bot Commands:
        
        Headlines:
        - "latest news" or "top headlines" - Get current top headlines
        - "news from [country]" - Get headlines from specific country (us, uk, ca, etc.)
        
        Search:
        - "news about [topic]" - Search for articles about specific topics
        - "search [keyword]" - Find articles containing keywords
        
        Sources:
        - "news sources" - Get list of available news sources
        - "sources for [category]" - Get sources by category (business, technology, etc.)
        - "news from [source]" - Get articles from specific news source
        
        Examples:
        - "What's the latest news?"
        - "News about climate change"
        - "Technology news sources"
        - "News from BBC"
        
        Note: You need a free API key from NewsAPI.org"""

# Create kernel and add services
kernel = sk.Kernel()
service_id = "oai_chat_gpt"
model_id = "gpt-4"

kernel.add_service(
    OpenAIChatCompletion(
        service_id=service_id,
        ai_model_id=model_id,
        api_key=api_key,
    ),
)

# Add news service plugin
news_service = NewsService()
kernel.add_plugin(news_service, "NewsService")

# Execution settings
execution_settings = OpenAIChatPromptExecutionSettings(
    service_id=service_id,
    ai_model_id=model_id,
    max_tokens=1500,
    temperature=0.7,
)

# Chat history
history = ChatHistory()
history.add_system_message("""You are a helpful news assistant that provides current news information from reliable sources. 
You can get headlines, search for specific topics, and provide news from various sources around the world.""")

chat_prompt = """
You are a news assistant with access to current news data from NewsAPI.

Chat History:
{{$history}}

User: {{$user_input}}

Help the user with news requests. Use the appropriate news functions:
- For latest headlines: use get_top_headlines
- For topic searches: use search_news
- For specific sources: use get_news_by_source
- For source lists: use get_news_sources
- For help: use get_news_help

Present news information in a clear, organized format with headlines, sources, and brief descriptions.
"""

def format_news_response(news_data: str) -> str:
    """Format news data into a readable response"""
    try:
        data = json.loads(news_data)
        
        if 'articles' in data:
            articles = data['articles']
            total = data.get('totalResults', len(articles))
            
            response = f"📰 Found {total} articles:\n\n"
            
            for i, article in enumerate(articles, 1):
                response += f"{i}. **{article['title']}**\n"
                response += f"   Source: {article['source']}\n"
                if article['description']:
                    response += f"   {article['description'][:150]}{'...' if len(article['description']) > 150 else ''}\n"
                if article['publishedAt']:
                    # Format date
                    try:
                        pub_date = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
                        response += f"   Published: {pub_date.strftime('%Y-%m-%d %H:%M UTC')}\n"
                    except:
                        response += f"   Published: {article['publishedAt']}\n"
                response += "\n"
            
            return response
        
        elif 'sources' in data:
            sources = data['sources']
            response = f"📡 Available News Sources ({len(sources)}):\n\n"
            
            for i, source in enumerate(sources, 1):
                response += f"{i}. **{source['name']}** ({source['id']})\n"
                response += f"   Category: {source['category'].title()}, Country: {source['country'].upper()}\n"
                if source['description']:
                    response += f"   {source['description'][:100]}{'...' if len(source['description']) > 100 else ''}\n"
                response += "\n"
            
            return response
        
        else:
            return news_data
            
    except json.JSONDecodeError:
        return news_data

async def get_ai_response(user_input: str) -> str:
    """Get AI response with news capabilities"""
    history_text = "\n".join([f"{msg.role}: {msg.content}" for msg in history.messages])
    final_prompt = chat_prompt.replace("{{$history}}", history_text).replace("{{$user_input}}", user_input)
    
    user_input_lower = user_input.lower()
    additional_context = ""
    
    # Parse user request and call appropriate news functions
    import re
    
    if any(phrase in user_input_lower for phrase in ['latest news', 'top headlines', 'current news']):
        # Check for country specification
        country = 'us'  # default
        country_match = re.search(r'(?:from|in) ([a-z]{2})', user_input_lower)
        if country_match:
            country = country_match.group(1)
        
        news_data = news_service.get_top_headlines(country)
        formatted_news = format_news_response(news_data)
        additional_context += f"\n{formatted_news}"
    
    elif 'news about' in user_input_lower or 'search' in user_input_lower:
        # Extract search topic
        topic_match = re.search(r'(?:news about|search (?:for )?)(.*?)(?:\?|$)', user_input_lower)
        if topic_match:
            topic = topic_match.group(1).strip()
            news_data = news_service.search_news(topic)
            formatted_news = format_news_response(news_data)
            additional_context += f"\n{formatted_news}"
    
    elif 'news sources' in user_input_lower or 'sources' in user_input_lower:
        # Check for category
        category = ""
        categories = ['business', 'technology', 'science', 'health', 'sports', 'entertainment']
        for cat in categories:
            if cat in user_input_lower:
                category = cat
                break
        
        sources_data = news_service.get_news_sources(category)
        formatted_sources = format_news_response(sources_data)
        additional_context += f"\n{formatted_sources}"
    
    elif 'news from' in user_input_lower:
        # Extract source name
        source_match = re.search(r'news from (.+?)(?:\?|$)', user_input_lower)
        if source_match:
            source = source_match.group(1).strip()
            # Convert common source names to IDs
            source_map = {
                'bbc': 'bbc-news',
                'cnn': 'cnn',
                'reuters': 'reuters',
                'bloomberg': 'bloomberg',
                'techcrunch': 'techcrunch',
                'wsj': 'the-wall-street-journal'
            }
            source_id = source_map.get(source.lower(), source.lower().replace(' ', '-'))
            
            news_data = news_service.get_news_by_source(source_id)
            formatted_news = format_news_response(news_data)
            additional_context += f"\n{formatted_news}"
    
    elif 'help' in user_input_lower or 'commands' in user_input_lower:
        help_info = news_service.get_news_help()
        additional_context += f"\n{help_info}"
    
    if additional_context:
        final_prompt += additional_context
    
    result = await kernel.invoke_prompt(
        prompt=final_prompt,
        settings=execution_settings
    )
    
    return str(result)

async def chat() -> bool:
    try:
        user_input = input("User:> ")
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting chat...")
        return False

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\n\nGoodbye! Stay informed! 📰")
        return False
    
    history.add_user_message(user_input)
    
    try:
        ai_response = await get_ai_response(user_input)
        print(f"NewsBot:> {ai_response}")
        history.add_assistant_message(ai_response)
    except Exception as e:
        print(f"NewsBot:> Sorry, I encountered an error: {e}")
    
    return True

async def main():
    print("📰 News Information Chat Bot 📰")
    print("Get the latest news from around the world!")
    print("\nExamples:")
    print("  - 'What's the latest news?'")
    print("  - 'News about artificial intelligence'")
    print("  - 'Technology news sources'")
    print("  - 'News from BBC'")
    print("\nType 'help' for more commands or 'exit' to quit.")
    print("=" * 50)
    
    chatting = True
    while chatting:
        chatting = await chat()

if __name__ == "__main__":
    asyncio.run(main())
