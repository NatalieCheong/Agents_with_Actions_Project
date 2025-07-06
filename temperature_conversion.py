import asyncio
import os
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

class TemperatureConverter:
    """Plugin for temperature conversions between Celsius and Fahrenheit"""
    
    @kernel_function(
        description="Converts temperature from Celsius to Fahrenheit",
        name="celsius_to_fahrenheit"
    )
    def celsius_to_fahrenheit(self, celsius: float) -> str:
        """Convert Celsius to Fahrenheit"""
        try:
            celsius_float = float(celsius)
            fahrenheit = (celsius_float * 9/5) + 32
            return f"{celsius}°C = {fahrenheit:.1f}°F"
        except ValueError:
            return "Invalid temperature value provided"
    
    @kernel_function(
        description="Converts temperature from Fahrenheit to Celsius", 
        name="fahrenheit_to_celsius"
    )
    def fahrenheit_to_celsius(self, fahrenheit: float) -> str:
        """Convert Fahrenheit to Celsius"""
        try:
            fahrenheit_float = float(fahrenheit)
            celsius = (fahrenheit_float - 32) * 5/9
            return f"{fahrenheit}°F = {celsius:.1f}°C"
        except ValueError:
            return "Invalid temperature value provided"
    
    @kernel_function(
        description="Gets information about temperature scales",
        name="get_temperature_info"
    )
    def get_temperature_info(self) -> str:
        """Provide information about temperature scales"""
        return """Temperature Scale Information:
        - Celsius (°C): Water freezes at 0°C and boils at 100°C
        - Fahrenheit (°F): Water freezes at 32°F and boils at 212°F
        - Conversion formulas:
          * C to F: (C × 9/5) + 32
          * F to C: (F - 32) × 5/9"""

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

# Add temperature converter plugin
temp_converter = TemperatureConverter()
kernel.add_plugin(temp_converter, "TemperatureConverter")

# Execution settings
execution_settings = OpenAIChatPromptExecutionSettings(
    service_id=service_id,
    ai_model_id=model_id,
    max_tokens=1000,
    temperature=0.7,
)

# Chat history
history = ChatHistory()
history.add_system_message("""You are a helpful temperature conversion assistant. You can help users convert between Celsius and Fahrenheit. 
When users ask for temperature conversions, use the available temperature converter functions to provide accurate results.""")

chat_prompt = """
You are a temperature conversion assistant with access to conversion tools.

Chat History:
{{$history}}

User: {{$user_input}}

Help the user with temperature conversions. If they provide a temperature value, use the appropriate conversion function.
For example:
- "25 celsius to fahrenheit" - use celsius_to_fahrenheit function
- "77 fahrenheit to celsius" - use fahrenheit_to_celsius function
- "temperature info" - use get_temperature_info function

Respond in a helpful and friendly manner.
"""

async def get_ai_response(user_input: str) -> str:
    """Get AI response with temperature conversion capabilities"""
    history_text = "\n".join([f"{msg.role}: {msg.content}" for msg in history.messages])
    final_prompt = chat_prompt.replace("{{$history}}", history_text).replace("{{$user_input}}", user_input)
    
    # Check if user is asking for temperature conversion
    user_input_lower = user_input.lower()
    additional_context = ""
    
    # Extract temperature values and detect conversion type
    import re
    
    # Look for patterns like "25 celsius" or "77 fahrenheit"
    celsius_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:c|celsius)', user_input_lower)
    fahrenheit_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:f|fahrenheit)', user_input_lower)
    
    if celsius_match and ('fahrenheit' in user_input_lower or 'f' in user_input_lower):
        temp_value = celsius_match.group(1)
        conversion_result = temp_converter.celsius_to_fahrenheit(temp_value)
        additional_context += f"\nConversion result: {conversion_result}"
    elif fahrenheit_match and ('celsius' in user_input_lower or 'c' in user_input_lower):
        temp_value = fahrenheit_match.group(1)
        conversion_result = temp_converter.fahrenheit_to_celsius(temp_value)
        additional_context += f"\nConversion result: {conversion_result}"
    elif 'temperature info' in user_input_lower or 'scale' in user_input_lower:
        temp_info = temp_converter.get_temperature_info()
        additional_context += f"\n{temp_info}"
    
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
        print("\n\nGoodbye! Stay warm! 🌡️")
        return False
    
    history.add_user_message(user_input)
    
    try:
        ai_response = await get_ai_response(user_input)
        print(f"TempBot:> {ai_response}")
        history.add_assistant_message(ai_response)
    except Exception as e:
        print(f"TempBot:> Sorry, I encountered an error: {e}")
    
    return True

async def main():
    print("🌡️ Temperature Conversion Chat Bot 🌡️")
    print("Ask me to convert temperatures between Celsius and Fahrenheit!")
    print("Examples:")
    print("  - '25 celsius to fahrenheit'")
    print("  - '77 fahrenheit to celsius'") 
    print("  - 'temperature info'")
    print("Type 'exit' to quit.")
    print("=" * 50)
    
    chatting = True
    while chatting:
        chatting = await chat()

if __name__ == "__main__":
    asyncio.run(main())
