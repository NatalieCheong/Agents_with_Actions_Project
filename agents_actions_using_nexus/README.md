# Agent Actions with Nexus Integration

This project demonstrates integrating third-party APIs into the Nexus AI framework, creating custom agent actions for weather, news, and movie information. The implementation showcases advanced AI agent capabilities with real-time data integration.

## 🌟 Features

- **Weather API Integration**: Real-time weather data from OpenWeatherMap
- **News API Integration**: Latest news headlines from NewsAPI
- **Movie API Integration**: Movie information from The Movie Database (TMDb)
- **Custom Agent Profile**: Professor Chronos - A historian with API capabilities
- **Error Handling**: Comprehensive error management for all API integrations
- **Dynamic Discovery**: Follows Nexus plugin architecture for seamless integration

## 🔧 Technologies Used

- **Nexus AI Framework** - AI agent orchestration platform
- **OpenAI GPT** - Large language model for AI capabilities
- **Python 3.8+** - Programming language
- **External APIs:**
  - OpenWeatherMap API (Weather data)
  - NewsAPI.org (News articles)
  - The Movie Database (TMDb) API (Movie information)

## 📋 Prerequisites

- Python 3.8 or higher
- Nexus framework installed and configured
- OpenAI API key
- Additional API keys for full functionality (see Setup section)
- Internet connection for API calls

## 🚀 Setup Instructions

### 1. Clone Nexus Framework

```bash
git clone https://github.com/cxbxmxcx/Nexus.git
cd Nexus
pip install -e .
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
WEATHER_API_KEY=your_openweather_api_key
NEWS_API_KEY=your_newsapi_key
TMDB_API_KEY=your_tmdb_api_key
```

### 4. Install Custom Actions

1. Copy the action files to the Nexus actions directory:
   ```bash
   cp get_weather.py get_news.py get_movie_info.py Nexus/nexus/nexus_base/nexus_actions/
   ```

2. Copy the agent profile to the profiles directory:
   ```bash
   cp historian.yaml Nexus/nexus/nexus_base/nexus_profiles/
   ```

### 5. Run Nexus

```bash
nexus run
```

## 📖 Usage

### Getting Started

1. **Select Agent Profile**: Choose "Professor Chronos" as your agent profile
2. **Configure Actions**: In Agent Settings, select the actions: `get_weather`, `get_news`, `get_movie_info`
3. **Start Interacting**: Begin asking questions to test the integrations

### Example Commands

- **Weather Queries:**
  - "What's the weather in New York?"
  - "Temperature in London today"
  - "Is it raining in Tokyo?"

- **News Queries:**
  - "Get me the latest news"
  - "What's happening in technology?"
  - "Show me news about artificial intelligence"

- **Movie Queries:**
  - "Tell me about the movie Inception"
  - "What's the rating for The Dark Knight?"
  - "When was Titanic released?"

## 🔌 API Integrations

### Weather API (OpenWeatherMap)
- **Features**: Current weather conditions, temperature, humidity, weather descriptions
- **Setup**: Get free API key from [OpenWeatherMap](https://openweathermap.org/api)
- **Error Handling**: Network timeouts, invalid city names, API rate limits

### News API (NewsAPI.org)
- **Features**: Latest news headlines, customizable queries, multiple sources
- **Setup**: Get free API key from [NewsAPI.org](https://newsapi.org/)
- **Error Handling**: Invalid queries, source limitations, request failures

### Movie Database API (TMDb)
- **Features**: Comprehensive movie information, ratings, release dates, overviews
- **Setup**: Get free API key from [The Movie Database](https://www.themoviedb.org/documentation/api)
- **Error Handling**: Movie not found, API timeouts, malformed responses

### File Descriptions

**`get_weather.py`**
- Weather API integration using OpenWeatherMap
- Handles city-based weather queries
- Includes temperature conversion and weather descriptions
- Comprehensive error handling for API failures

**`get_news.py`**
- News API integration with NewsAPI.org
- Supports topic-based and general news queries
- Formats news articles with headlines and descriptions
- Error handling for API limitations and network issues

**`get_movie_info.py`**
- Movie database integration using TMDb API
- Retrieves movie information including ratings and summaries
- Handles movie search and detailed information retrieval
- Robust error handling for missing or invalid movie data

**`historian.yaml`**
- Custom agent profile configuration
- Defines Professor Chronos character and capabilities
- Specifies available actions and behavioral parameters

## 🛠️ Technical Details

- **Framework**: Built using the Nexus AI framework architecture
- **Decorators**: Uses `@agent_action` decorator for function registration
- **Environment Management**: Proper environment variable handling with `.env` files
- **Type Hints**: Comprehensive type annotations for better code documentation
- **Plugin Architecture**: Follows Nexus plugin system for dynamic discovery
- **Error Handling**: Implements comprehensive error management across all integrations

## 🔧 API Key Setup

### OpenAI API Key
Get your API key from [OpenAI Platform](https://platform.openai.com/)

### Weather API Key
Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)

### News API Key
Get a free API key from [NewsAPI.org](https://newsapi.org/)

### Movie Database API Key
Get a free API key from [The Movie Database](https://www.themoviedb.org/documentation/api)

## 🎯 Quick Start

1. **Set up your API keys** in the `.env` file
2. **Run the Nexus framework:**
   ```bash
   nexus run
   ```
3. **Select Professor Chronos** as your agent
4. **Enable the actions** in Agent Settings
5. **Start asking questions** like "What's the weather in Paris?"

## 💡 Key Concepts

Each component demonstrates important Nexus framework concepts:

- **Agent Actions**: Creating reusable, modular API integrations
- **Function Decorators**: Using `@agent_action` for AI integration
- **API Integration**: Connecting external services seamlessly
- **Error Handling**: Robust error management and fallbacks
- **Profile Configuration**: Building custom agent personalities
- **Dynamic Discovery**: Leveraging Nexus plugin architecture

## 🐛 Troubleshooting

If you encounter any issues:

- **Check API Keys**: Ensure all API keys are properly configured in `.env`
- **Verify Dependencies**: Make sure you have the latest dependencies installed
- **Review Error Messages**: Check console output for specific guidance
- **Test Individual APIs**: Verify each API key works independently
- **Check Network**: Ensure stable internet connection for API calls

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Nexus AI Framework team for the excellent agent platform
- OpenAI for providing powerful language models
- API providers: OpenWeatherMap, NewsAPI.org, and The Movie Database
- Open source community for continuous inspiration

Built with ❤️ using Nexus AI Framework and OpenAI
