import asyncio
import os
import json
import requests
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

class NutritionService:
    """Native functions for fetching nutritional information"""
    
    def __init__(self):
        # Using USDA FoodData Central API (free, no key required for basic access)
        self.base_url = "https://api.nal.usda.gov/fdc/v1"
        # You can get a free API key from https://fdc.nal.usda.gov/api-guide.html
        self.api_key = os.getenv('USDA_API_KEY', 'DEMO_KEY')
    
    @kernel_function(
        description="Gets nutritional information for a specific food item",
        name="get_nutrition_info"
    )
    def get_nutrition_info(self, food_item: str) -> str:
        """Get nutritional information for a food item"""
        try:
            # Search for food item
            search_url = f"{self.base_url}/foods/search"
            params = {
                'query': food_item,
                'api_key': self.api_key,
                'pageSize': 1
            }
            
            response = requests.get(search_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['foods']:
                    food = data['foods'][0]
                    
                    # Extract key nutrients
                    nutrients = {}
                    for nutrient in food.get('foodNutrients', []):
                        name = nutrient.get('nutrientName', '')
                        value = nutrient.get('value', 0)
                        unit = nutrient.get('unitName', '')
                        
                        # Focus on key nutrients
                        if any(key in name.lower() for key in ['energy', 'protein', 'fat', 'carbohydrate', 'fiber', 'sugar', 'sodium', 'vitamin', 'calcium', 'iron']):
                            nutrients[name] = f"{value} {unit}"
                    
                    nutrition_info = {
                        'food_name': food.get('description', food_item),
                        'brand': food.get('brandOwner', 'Generic'),
                        'nutrients': nutrients
                    }
                    
                    return json.dumps(nutrition_info)
                else:
                    return f"No nutritional information found for '{food_item}'"
            else:
                # Fallback with estimated nutrition data
                return self._get_estimated_nutrition(food_item)
                
        except Exception as e:
            return self._get_estimated_nutrition(food_item)
    
    def _get_estimated_nutrition(self, food_item: str) -> str:
        """Fallback method with estimated nutrition data"""
        # Basic nutrition estimates for common foods
        nutrition_db = {
            'chicken breast': {'calories': '165', 'protein': '31g', 'fat': '3.6g', 'carbs': '0g'},
            'salmon': {'calories': '208', 'protein': '22g', 'fat': '12g', 'carbs': '0g'},
            'rice': {'calories': '130', 'protein': '2.7g', 'fat': '0.3g', 'carbs': '28g'},
            'broccoli': {'calories': '34', 'protein': '2.8g', 'fat': '0.4g', 'carbs': '7g'},
            'apple': {'calories': '52', 'protein': '0.3g', 'fat': '0.2g', 'carbs': '14g'},
            'banana': {'calories': '89', 'protein': '1.1g', 'fat': '0.3g', 'carbs': '23g'},
            'oats': {'calories': '389', 'protein': '17g', 'fat': '7g', 'carbs': '66g'},
            'egg': {'calories': '155', 'protein': '13g', 'fat': '11g', 'carbs': '1.1g'},
            'milk': {'calories': '42', 'protein': '3.4g', 'fat': '1g', 'carbs': '5g'},
            'bread': {'calories': '265', 'protein': '9g', 'fat': '3.2g', 'carbs': '49g'}
        }
        
        food_lower = food_item.lower()
        for key, nutrition in nutrition_db.items():
            if key in food_lower or food_lower in key:
                nutrition_info = {
                    'food_name': food_item,
                    'brand': 'Estimated',
                    'nutrients': nutrition,
                    'note': 'Estimated values per 100g'
                }
                return json.dumps(nutrition_info)
        
        # Generic fallback
        nutrition_info = {
            'food_name': food_item,
            'brand': 'Unknown',
            'nutrients': {'calories': 'Data not available'},
            'note': 'Nutritional information not found'
        }
        return json.dumps(nutrition_info)
    
    @kernel_function(
        description="Calculates total calories for a list of food items",
        name="calculate_total_calories"
    )
    def calculate_total_calories(self, food_list: str) -> str:
        """Calculate total calories for multiple food items"""
        foods = [food.strip() for food in food_list.split(',')]
        total_calories = 0
        details = []
        
        for food in foods:
            nutrition_data = self.get_nutrition_info(food)
            try:
                nutrition = json.loads(nutrition_data)
                nutrients = nutrition.get('nutrients', {})
                
                # Extract calories
                calories = 0
                for key, value in nutrients.items():
                    if 'energy' in key.lower() or 'calorie' in key.lower():
                        # Extract numeric value
                        import re
                        match = re.search(r'(\d+)', str(value))
                        if match:
                            calories = int(match.group(1))
                            break
                
                if calories == 0 and 'calories' in nutrients:
                    match = re.search(r'(\d+)', str(nutrients['calories']))
                    if match:
                        calories = int(match.group(1))
                
                total_calories += calories
                details.append(f"{food}: {calories} calories")
                
            except:
                details.append(f"{food}: calories unknown")
        
        result = {
            'total_calories': total_calories,
            'breakdown': details
        }
        
        return json.dumps(result)

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

# Add nutrition service plugin
nutrition_service = NutritionService()
kernel.add_plugin(nutrition_service, "NutritionService")

# Execution settings
execution_settings = OpenAIChatPromptExecutionSettings(
    service_id=service_id,
    ai_model_id=model_id,
    max_tokens=1500,
    temperature=0.7,
)

# Semantic function for meal planning
meal_plan_prompt = """
You are a professional nutritionist and meal planning expert.

Create a balanced meal plan based on the following requirements:
- Goal: {{$goal}}
- Dietary preferences: {{$preferences}}
- Number of meals: {{$meals}}
- Any restrictions: {{$restrictions}}

Create a detailed meal plan that includes:
1. Breakfast, lunch, dinner (and snacks if requested)
2. Specific food items and portions
3. Variety and balance
4. Consideration of the stated goal and preferences

Make it practical and achievable. List specific ingredients for each meal.

Goal: {{$goal}}
Preferences: {{$preferences}}
Meals per day: {{$meals}}
Restrictions: {{$restrictions}}
"""

# Chat history
history = ChatHistory()
history.add_system_message("""You are a comprehensive nutrition and meal planning assistant. You combine AI-generated meal plans with real nutritional data to help users achieve their health goals. You can create meal plans and provide detailed nutritional information for foods.""")

async def create_enhanced_meal_plan(goal: str, preferences: str = "balanced diet", meals: str = "3", restrictions: str = "none") -> str:
    """Create a meal plan using semantic function"""
    final_prompt = meal_plan_prompt.replace("{{$goal}}", goal).replace("{{$preferences}}", preferences).replace("{{$meals}}", meals).replace("{{$restrictions}}", restrictions)
    
    result = await kernel.invoke_prompt(
        prompt=final_prompt,
        settings=execution_settings
    )
    
    return str(result)

async def get_ai_response(user_input: str) -> str:
    """Get AI response with meal planning and nutrition capabilities"""
    user_input_lower = user_input.lower()
    
    # Check for meal planning requests
    if any(word in user_input_lower for word in ['meal plan', 'diet plan', 'menu']):
        # Extract goal
        goal = "maintain healthy weight"
        if 'lose weight' in user_input_lower or 'weight loss' in user_input_lower:
            goal = "lose weight"
        elif 'gain weight' in user_input_lower or 'muscle' in user_input_lower:
            goal = "gain muscle mass"
        elif 'maintain' in user_input_lower:
            goal = "maintain current weight"
        
        # Extract preferences
        preferences = "balanced diet"
        if 'vegetarian' in user_input_lower:
            preferences = "vegetarian"
        elif 'vegan' in user_input_lower:
            preferences = "vegan"
        elif 'keto' in user_input_lower:
            preferences = "ketogenic"
        elif 'low carb' in user_input_lower:
            preferences = "low carb"
        
        # Create meal plan
        meal_plan = await create_enhanced_meal_plan(goal, preferences)
        
        # Extract food items from meal plan to get nutrition info
        import re
        food_items = []
        
        # Simple extraction of food items (this could be more sophisticated)
        common_foods = ['chicken', 'salmon', 'rice', 'broccoli', 'apple', 'banana', 'oats', 'egg', 'milk', 'bread']
        for food in common_foods:
            if food in meal_plan.lower():
                food_items.append(food)
        
        nutrition_info = ""
        if food_items:
            # Get nutrition for first few items
            for food in food_items[:3]:
                nutrition = nutrition_service.get_nutrition_info(food)
                try:
                    nutrition_data = json.loads(nutrition)
                    nutrition_info += f"\n\n📊 Nutrition for {nutrition_data['food_name']}:\n"
                    for nutrient, value in nutrition_data.get('nutrients', {}).items():
                        nutrition_info += f"  • {nutrient}: {value}\n"
                except:
                    pass
        
        return f"Here's your personalized meal plan:\n\n{meal_plan}{nutrition_info}"
    
    # Check for nutrition information requests
    elif 'nutrition' in user_input_lower or 'calories' in user_input_lower:
        # Extract food items
        import re
        
        # Look for food names
        food_match = re.search(r'nutrition (?:for |of |in )?(.+?)(?:\?|$)', user_input_lower)
        if not food_match:
            food_match = re.search(r'calories in (.+?)(?:\?|$)', user_input_lower)
        
        if food_match:
            food_item = food_match.group(1).strip()
            nutrition_data = nutrition_service.get_nutrition_info(food_item)
            
            try:
                nutrition = json.loads(nutrition_data)
                response = f"📊 Nutritional Information for {nutrition['food_name']}:\n\n"
                
                for nutrient, value in nutrition.get('nutrients', {}).items():
                    response += f"• {nutrient}: {value}\n"
                
                if nutrition.get('note'):
                    response += f"\nNote: {nutrition['note']}"
                    
                return response
            except:
                return f"Here's the nutrition information I found:\n{nutrition_data}"
    
    # Check for calorie calculation requests
    elif 'total calories' in user_input_lower or 'calculate calories' in user_input_lower:
        # Extract food list
        foods_match = re.search(r'(?:calories (?:for|in) |calculate calories (?:for )?)(.*?)(?:\?|$)', user_input_lower)
        if foods_match:
            food_list = foods_match.group(1).strip()
            calorie_data = nutrition_service.calculate_total_calories(food_list)
            
            try:
                data = json.loads(calorie_data)
                response = f"🧮 Total Calorie Calculation:\n\n"
                for item in data['breakdown']:
                    response += f"• {item}\n"
                response += f"\n🔥 Total Calories: {data['total_calories']}"
                return response
            except:
                return f"Calorie calculation: {calorie_data}"
    
    # Regular chat response
    chat_prompt = f"""
    You are a nutrition and meal planning assistant. The user said: "{user_input}"
    
    Provide helpful guidance about nutrition, meal planning, or healthy eating. 
    If they haven't made a specific request, encourage them to ask for:
    - Meal plans (e.g., "Create a meal plan for weight loss")
    - Nutrition information (e.g., "What's the nutrition in chicken breast?")
    - Calorie calculations (e.g., "Calculate calories for apple, banana, oats")
    
    Be encouraging and provide practical advice.
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
        print("\n\nGoodbye! Stay healthy! 🥗")
        return False
    
    history.add_user_message(user_input)
    
    try:
        ai_response = await get_ai_response(user_input)
        print(f"NutritionBot:> {ai_response}")
        history.add_assistant_message(ai_response)
    except Exception as e:
        print(f"NutritionBot:> Sorry, I encountered an error: {e}")
    
    return True

async def main():
    print("🥗 Enhanced Nutrition & Meal Planning Assistant 🥗")
    print("I combine AI meal planning with real nutritional data!")
    print("\nExamples:")
    print("  - 'Create a meal plan for weight loss'")
    print("  - 'What's the nutrition in salmon?'")
    print("  - 'Calculate calories for chicken, rice, broccoli'")
    print("  - 'Make a vegetarian meal plan'")
    print("\nType 'exit' to quit.")
    print("=" * 60)
    
    chatting = True
    while chatting:
        chatting = await chat()

if __name__ == "__main__":
    asyncio.run(main())
