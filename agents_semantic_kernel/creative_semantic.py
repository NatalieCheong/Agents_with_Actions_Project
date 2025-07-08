import asyncio
import os
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.contents.chat_history import ChatHistory

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

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

# Execution settings
execution_settings = OpenAIChatPromptExecutionSettings(
    service_id=service_id,
    ai_model_id=model_id,
    max_tokens=1500,
    temperature=0.8,  # Higher temperature for creativity
)

# Creative semantic function prompts
poem_prompt = """
You are a talented poet who writes beautiful, creative poems based on user themes.

Create a poem about: {{$theme}}

Guidelines:
- Make it emotionally engaging and vivid
- Use creative metaphors and imagery
- Choose an appropriate style (rhyming, free verse, haiku, etc.)
- Length should be 12-20 lines
- Make it memorable and meaningful

Theme: {{$theme}}
Additional style notes: {{$style}}
"""

story_prompt = """
You are a wonderful children's story writer who creates engaging, age-appropriate stories.

Write a children's story about: {{$topic}}

Guidelines:
- Make it suitable for ages 5-10
- Include a positive message or lesson
- Use simple, engaging language
- Create memorable characters
- Include some dialogue
- Make it fun and imaginative
- Length: 200-300 words

Topic: {{$topic}}
Main character: {{$character}}
Setting: {{$setting}}
"""

creative_writing_prompt = """
You are a creative writing assistant who helps with various forms of creative expression.

Writing request: {{$request}}

Create engaging, original content that:
- Captures the reader's attention
- Uses vivid descriptions and engaging language
- Follows appropriate structure for the format
- Is creative and imaginative
- Meets the specific requirements mentioned

Additional details: {{$details}}
"""

# Chat history
history = ChatHistory()
history.add_system_message("""You are a creative writing assistant specializing in poems and children's stories. 
You help users create beautiful, engaging content based on their ideas and themes.""")

async def create_poem(theme: str, style: str = "free verse") -> str:
    """Create a poem based on theme and style"""
    final_prompt = poem_prompt.replace("{{$theme}}", theme).replace("{{$style}}", style)
    
    result = await kernel.invoke_prompt(
        prompt=final_prompt,
        settings=execution_settings
    )
    
    return str(result)

async def create_story(topic: str, character: str = "a friendly animal", setting: str = "a magical forest") -> str:
    """Create a children's story"""
    final_prompt = story_prompt.replace("{{$topic}}", topic).replace("{{$character}}", character).replace("{{$setting}}", setting)
    
    result = await kernel.invoke_prompt(
        prompt=final_prompt,
        settings=execution_settings
    )
    
    return str(result)

async def create_custom_content(request: str, details: str = "") -> str:
    """Create custom creative content"""
    final_prompt = creative_writing_prompt.replace("{{$request}}", request).replace("{{$details}}", details)
    
    result = await kernel.invoke_prompt(
        prompt=final_prompt,
        settings=execution_settings
    )
    
    return str(result)

def parse_creative_request(user_input: str):
    """Parse user input to determine what type of creative content to generate"""
    user_input_lower = user_input.lower()
    
    if 'poem' in user_input_lower:
        return 'poem'
    elif 'story' in user_input_lower or 'tale' in user_input_lower:
        return 'story'
    elif 'write' in user_input_lower or 'create' in user_input_lower:
        return 'custom'
    else:
        return 'chat'

async def get_ai_response(user_input: str) -> str:
    """Get AI response for creative writing requests"""
    
    request_type = parse_creative_request(user_input)
    
    if request_type == 'poem':
        # Extract theme from user input
        import re
        theme_match = re.search(r'poem about (.+?)(?:\.|$|\?)', user_input.lower())
        if theme_match:
            theme = theme_match.group(1).strip()
        else:
            # Try alternative patterns
            words = user_input.lower().replace('poem', '').replace('write', '').replace('create', '').strip()
            theme = words if words else "life and dreams"
        
        # Check for style preferences
        style = "free verse"
        if 'haiku' in user_input.lower():
            style = "haiku"
        elif 'rhyme' in user_input.lower() or 'rhyming' in user_input.lower():
            style = "rhyming verse"
        elif 'sonnet' in user_input.lower():
            style = "sonnet"
        
        result = await create_poem(theme, style)
        return f"Here's a {style} poem about {theme}:\n\n{result}"
    
    elif request_type == 'story':
        # Extract story elements
        import re
        topic_match = re.search(r'story about (.+?)(?:\.|$|\?)', user_input.lower())
        if topic_match:
            topic = topic_match.group(1).strip()
        else:
            words = user_input.lower().replace('story', '').replace('write', '').replace('create', '').strip()
            topic = words if words else "a magical adventure"
        
        # Extract character if mentioned
        character = "a friendly animal"
        if 'dragon' in user_input.lower():
            character = "a kind dragon"
        elif 'princess' in user_input.lower():
            character = "a brave princess"
        elif 'cat' in user_input.lower():
            character = "a clever cat"
        elif 'dog' in user_input.lower():
            character = "a loyal dog"
        
        # Extract setting if mentioned
        setting = "a magical forest"
        if 'castle' in user_input.lower():
            setting = "a grand castle"
        elif 'ocean' in user_input.lower() or 'sea' in user_input.lower():
            setting = "under the sea"
        elif 'space' in user_input.lower():
            setting = "in outer space"
        
        result = await create_story(topic, character, setting)
        return f"Here's a children's story about {topic}:\n\n{result}"
    
    elif request_type == 'custom':
        result = await create_custom_content(user_input, "User requested custom creative content")
        return result
    
    else:
        # Regular chat response
        chat_prompt = f"""
        You are a friendly creative writing assistant. The user said: "{user_input}"
        
        Respond helpfully about creative writing. If they haven't made a specific request, 
        encourage them to ask for a poem, story, or other creative content.
        
        Examples of what you can help with:
        - "Write a poem about sunshine"
        - "Create a story about a magical cat"
        - "Write a haiku about rain"
        - "Tell a story about friendship"
        """
        
        result = await kernel.invoke_prompt(
            prompt=chat_prompt,
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
        print("\n\nGoodbye! Keep creating! ✨")
        return False
    
    history.add_user_message(user_input)
    
    try:
        ai_response = await get_ai_response(user_input)
        print(f"CreativeBot:> {ai_response}")
        history.add_assistant_message(ai_response)
    except Exception as e:
        print(f"CreativeBot:> Sorry, I encountered an error: {e}")
    
    return True

async def main():
    print("✨ Creative Writing Assistant ✨")
    print("I can help you create poems and children's stories!")
    print("\nExamples:")
    print("  - 'Write a poem about the ocean'")
    print("  - 'Create a story about a brave mouse'")
    print("  - 'Write a haiku about spring'")
    print("  - 'Tell a story about friendship'")
    print("\nType 'exit' to quit.")
    print("=" * 50)
    
    chatting = True
    while chatting:
        chatting = await chat()

if __name__ == "__main__":
    asyncio.run(main())
