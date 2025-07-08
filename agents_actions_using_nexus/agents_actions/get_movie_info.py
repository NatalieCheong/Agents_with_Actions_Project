import requests
import os
from dotenv import load_dotenv
from nexus.nexus_base.action_manager import agent_action

load_dotenv()

@agent_action
def get_movie_info(movie_title: str) -> str:
    """Get movie information from The Movie Database (TMDb)."""
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        return "❌ Error: TMDB_API_KEY not found in environment variables"
    
    search_url = "https://api.themoviedb.org/3/search/movie"
    
    try:
        params = {
            'api_key': api_key,
            'query': movie_title
        }
        
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if not data['results']:
            return f"🎬 No movies found for '{movie_title}'"
        
        movie = data['results'][0]
        
        title = movie['title']
        release_date = movie.get('release_date', 'Unknown')
        overview = movie.get('overview', 'No overview available')
        rating = movie.get('vote_average', 'N/A')
        vote_count = movie.get('vote_count', 0)
        
        movie_info = f"""🎬 Movie Information:
**{title}** ({release_date[:4] if release_date != 'Unknown' else 'Unknown'})

Rating: ⭐ {rating}/10 ({vote_count} votes)

Overview: {overview}"""
        
        return movie_info
        
    except Exception as e:
        return f"❌ Error fetching movie data: {str(e)}"

