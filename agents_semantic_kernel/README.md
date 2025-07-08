# Semantic Kernel Exercises

A collection of practical project demonstrating Microsoft Semantic Kernel capabilities with OpenAI integration. These showcase plugin development, API integration, and the combination of semantic and native functions.

## 🚀 Project Overview

This repository contains 5 comprehensive exercises that demonstrate different aspects of Semantic Kernel development:

1. **Temperature Conversion Plugin** - Basic plugin creation with native functions
2. **Weather Information Plugin** - Real-time API integration with error handling
3. **Creative Semantic Functions** - AI-powered creative writing assistance
4. **Enhanced Nutrition & Meal Planning** - Combining semantic and native functions
5. **News API Wrapper** - Professional API wrapping with comprehensive functionality

## 🛠️ Technologies Used

- **Microsoft Semantic Kernel** - AI orchestration framework
- **OpenAI GPT-4** - Large language model for AI capabilities
- **Python 3.11+** - Programming language
- **External APIs**:
  - OpenWeatherMap API (Weather data)
  - NewsAPI.org (News articles)
  - USDA FoodData Central API (Nutrition information)

## 📋 Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Additional API keys for full functionality (see Setup section)

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/semantic-kernel-exercises.git
   cd semantic-kernel-exercises
   ```

2. **Install dependencies**:
   ```bash
   pip install semantic-kernel python-dotenv requests
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   WEATHER_API_KEY=your_openweather_api_key  # Optional for Exercise 2
   NEWS_API_KEY=your_newsapi_key             # Optional for Exercise 5
   USDA_API_KEY=your_usda_api_key           # Optional for Exercise 4
   ```

## 🎯 Exercise Descriptions

### Exercise 1: Temperature Conversion Plugin
**File**: `temperature_conversion.py`

A basic plugin demonstrating fundamental Semantic Kernel concepts with temperature conversion between Celsius and Fahrenheit.

**Features**:
- Convert Celsius to Fahrenheit
- Convert Fahrenheit to Celsius
- Temperature scale information
- Interactive chat interface

**Usage**:
```bash
python temperature_conversion.py
```

**Example commands**:
- "25 celsius to fahrenheit"
- "77 fahrenheit to celsius"
- "temperature info"

### Exercise 2: Weather Information Plugin
**File**: `weather_plugin.py`

Real-time weather information integration using OpenWeatherMap API.

**Features**:
- Current weather conditions
- 5-day weather forecast
- Multiple city support
- Error handling and fallbacks

**Setup**: Get free API key from [OpenWeatherMap](https://openweathermap.org/api)

**Usage**:
```bash
python weather_plugin.py
```

**Example commands**:
- "What's the weather in London?"
- "Temperature in New York"
- "Forecast for Tokyo"

### Exercise 3: Creative Semantic Functions
**File**: `creative_semantic.py`

AI-powered creative writing assistant for poems and children's stories.

**Features**:
- Generate custom poems (various styles)
- Create children's stories
- Creative writing assistance
- Customizable themes and characters

**Usage**:
```bash
python creative_semantic.py
```

**Example commands**:
- "Write a poem about the ocean"
- "Create a story about a brave mouse"
- "Write a haiku about spring"

### Exercise 4: Enhanced Semantic Functions with Native Functions
**File**: `enhanced_semantic_native.py`

Advanced integration combining AI meal planning with real nutritional data.

**Features**:
- AI-generated meal plans
- Real nutritional information lookup
- Calorie calculations
- Dietary preference support
- USDA database integration

**Usage**:
```bash
python enhanced_semantic_native.py
```

**Example commands**:
- "Create a meal plan for weight loss"
- "What's the nutrition in salmon?"
- "Calculate calories for chicken, rice, broccoli"

### Exercise 5: News API Wrapper
**File**: `news_api_wrapper.py`

Professional news service integration with comprehensive functionality.

**Features**:
- Latest headlines by country
- Topic-based news search
- Source-specific news
- Multiple news sources
- Formatted news presentation

**Setup**: Get free API key from [NewsAPI.org](https://newsapi.org/)

**Usage**:
```bash
python news_api_wrapper.py
```

**Example commands**:
- "What's the latest news?"
- "News about artificial intelligence"
- "Technology news sources"

## 🔑 API Keys Setup

### Required:
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/)

### Optional (for enhanced functionality):
- **Weather API**: Free at [OpenWeatherMap](https://openweathermap.org/api)
- **News API**: Free at [NewsAPI.org](https://newsapi.org/)
- **USDA API**: Free at [FoodData Central](https://fdc.nal.usda.gov/api-guide.html)

## 🏃‍♂️ Quick Start

1. Set up your OpenAI API key in `.env`
2. Run any exercise file:
   ```bash
   python temperature_conversion.py
   ```
3. Follow the interactive prompts
4. Type 'exit' to quit any exercise

## 📚 Learning Objectives

Each exercise demonstrates key Semantic Kernel concepts:

- **Plugin Architecture**: Creating reusable, modular components
- **Function Decorators**: Using `@kernel_function` for AI integration
- **API Integration**: Connecting external services seamlessly
- **Error Handling**: Robust error management and fallbacks
- **Chat Interfaces**: Building conversational AI applications
- **Semantic Functions**: Leveraging AI for complex reasoning
- **Native Functions**: Combining traditional programming with AI

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Microsoft Semantic Kernel team for the excellent framework
- OpenAI for providing powerful language models
- API providers: OpenWeatherMap, NewsAPI.org, and USDA FoodData Central

## 📞 Support

If you encounter any issues:
1. Check that all API keys are properly configured
2. Ensure you have the latest dependencies installed
3. Review the error messages for specific guidance
4. Open an issue in this repository

---

**Built with ❤️ using Microsoft Semantic Kernel and OpenAI**
