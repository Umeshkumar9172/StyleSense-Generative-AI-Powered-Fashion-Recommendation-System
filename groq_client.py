import os
import re
import json
from urllib.parse import urlparse, quote
from groq import Groq
from dotenv import load_dotenv
import traceback

load_dotenv()

class GroqService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        print(f"GroqService initialized. API Key available: {bool(self.api_key)}")
        if not self.api_key:
            print("  Warning: No API key found in environment")
            self.client = None
        else:
            print("  Creating Groq client...")
            self.client = Groq(api_key=self.api_key)

    def set_api_key(self, api_key):
        self.client = Groq(api_key=api_key)

    def get_fashion_recommendations(self, skin_tone, gender, face_shape="Oval", context=""):
        if not self.client:
            print("Error: Groq client not initialized")
            return {"success": False, "message": "Groq API Key is missing."}

        print(f"\nGenerating advanced recommendations for: {gender} with {skin_tone} skin tone and {face_shape} face shape")

        system_prompt = f"""
You are an advanced AI Fashion Stylist and Shopping Recommendation Engine. 
  
 Your task is to generate highly personalized, realistic, and actionable fashion recommendations based on user attributes. 
  
 ----------------------------------- 
 🧠 INPUT: 
 - Gender: {gender} 
 - Skin Tone: {skin_tone}  (e.g., fair, medium, olive, dark) 
 - Face Shape: {face_shape} (e.g., oval, round, square, heart) 
  
 ----------------------------------- 
 🎯 OBJECTIVE: 
 Generate: 
 1. Personalized style analysis 
 2. Occasion-based outfit recommendations 
 3. Real shopping suggestions from major platforms 
 4. Clean structured JSON output for frontend use 
  
 ----------------------------------- 
 🚨 STRICT RULES: 
  
 1. Gender-Specific Filtering: 
    - If Gender = Female → suggest saree, kurti, dresses, heels, handbags 
    - If Gender = Male → suggest shirts, jeans, trousers, sneakers, watches 
  
 2. Regional Relevance: 
    - Focus on realistic fashion trends (India + global) 
    - Include ethnic + western mix 
  
 3. Smart Color Matching: 
    - Olive → earthy tones, jewel tones 
    - Fair → pastels, soft tones 
    - Dark → bold & vibrant colors 
    - Medium → balanced palette 
  
 4. Output MUST be practical (no fantasy styling) 
  
 5. Do NOT generate long paragraphs 
    Keep responses crisp, structured, and UI-friendly 
  
 ----------------------------------- 
 🛒 SHOPPING INTEGRATION RULES: 
  
 For EACH product: 
 - Must include real platform name: 
   Amazon, Flipkart, Myntra, Ajio 
  
 - Generate SEARCH LINKS (NOT fake product links): 
  
 Amazon: 
 `https://www.amazon.in/s?k={{search_query}}`  
  
 Flipkart: 
 `https://www.flipkart.com/search?q={{search_query}}`  
  
 Myntra: 
 `https://www.myntra.com/{{search_query}}`  
  
 Ajio: 
 `https://www.ajio.com/search/?text={{search_query}}`  
  
 Replace spaces with "+" in query. 
  
 ----------------------------------- 
 📦 OUTPUT FORMAT (STRICT JSON ONLY): 
  
 {{ 
   "analysis": {{ 
     "style_summary": "Short personalized insight (2-3 lines max)", 
     "color_recommendation": ["color1", "color2", "color3"], 
     "avoid_colors": ["color1", "color2"] 
   }}, 
  
   "outfits": [ 
     {{ 
       "occasion": "Casual", 
       "items": [ 
         {{ 
           "item_name": "Mustard Cotton Kurti", 
           "category": "Topwear", 
           "color": "Mustard Yellow", 
           "reason": "Enhances warm olive undertone", 
           "platform": "Myntra", 
           "search_link": "https://www.myntra.com/mustard+kurti+women" 
         }}, 
         {{ 
           "item_name": "Blue Straight Fit Jeans", 
           "category": "Bottomwear", 
           "color": "Blue", 
           "reason": "Balances bright top", 
           "platform": "Flipkart", 
           "search_link": "https://www.flipkart.com/search?q=blue+jeans+women" 
         }} 
       ] 
     }}, 
     {{ 
       "occasion": "Party", 
       "items": [
         {{ 
           "item_name": "Evening Dress", 
           "category": "Full Body", 
           "color": "Emerald Green", 
           "reason": "Complements skin tone", 
           "platform": "Ajio", 
           "search_link": "https://www.ajio.com/search/?text=emerald+green+dress" 
         }}
       ] 
     }}, 
     {{ 
       "occasion": "Office", 
       "items": [
         {{ 
           "item_name": "Formal Blazer", 
           "category": "Topwear", 
           "color": "Navy Blue", 
           "reason": "Professional look", 
           "platform": "Amazon", 
           "search_link": "https://www.amazon.in/s?k=navy+blue+blazer" 
         }}
       ] 
     }} 
   ], 
  
   "accessories": [ 
     {{ 
       "item_name": "Gold Hoop Earrings", 
       "reason": "Complements warm undertone", 
       "platform": "Amazon", 
       "search_link": "https://www.amazon.in/s?k=gold+hoop+earrings" 
     }} 
   ], 
  
   "styling_tips": [ 
     "Keep outfits balanced with 2-3 colors max", 
     "Use layers to add depth", 
     "Choose fabrics based on season" 
   ] 
 }} 
  
 ----------------------------------- 
 🚨 CRITICAL INSTRUCTIONS: 
 - You MUST return ALL the keys: "analysis", "outfits", "accessories", "styling_tips".
 - The "outfits" array MUST contain at least 3 occasions: "Casual", "Party", "Office".
 - Each occasion MUST have at least 2 items in the "items" array.
 - DO NOT include any text outside of the JSON object.
 - DO NOT include markdown formatting like ```json.
 - Ensure all search links follow the exact format provided.
"""
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": f"Provide fashion recommendations for a {gender} with {skin_tone} skin tone and {face_shape} face shape.",
                    }
                ],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            response_text = chat_completion.choices[0].message.content
            
            # Clean response text just in case markdown is present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            print(f"DEBUG - Groq response JSON: {response_text}")
            try:
                data = json.loads(response_text)
                
                # If the AI wrapped everything in a top-level key
                if isinstance(data, dict) and len(data.keys()) == 1:
                    top_key = list(data.keys())[0].lower()
                    if any(k in top_key for k in ["recommendation", "data", "result", "fashion", "style", "stylist", "guide", "advice"]):
                        data = data[list(data.keys())[0]]
                        print(f"DEBUG - Unwrapped JSON using key '{list(data.keys())[0]}': {data}")
                
                return data
            except json.JSONDecodeError as je:
                print(f"JSON Decode Error: {je}")
                # Try to find JSON object in text if loads failed
                match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if match:
                    data = json.loads(match.group())
                    # Same unwrapping logic for the regex match
                    if isinstance(data, dict) and len(data.keys()) == 1:
                        top_key = list(data.keys())[0].lower()
                        if any(k in top_key for k in ["recommendation", "data", "result", "fashion", "style", "stylist", "guide", "advice"]):
                            data = data[list(data.keys())[0]]
                    return data
                raise je
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            return {"success": False, "message": "Could not get recommendations from Groq."}



    def get_chat_response(self, user_message, chat_history=None):
        if not self.client:
            return "Error: Groq API Key is missing."

        if chat_history is None:
            chat_history = []

        system_prompt = {
            "role": "system",
            "content": "You are StyleBot, a friendly and helpful fashion assistant. Your goal is to help users with fashion advice, outfit ideas, and style tips. Be concise, professional, and encouraging. If users ask about their specific skin tone or face shape, remind them to use the 'Analyze & Style Me!' feature for personalized results."
        }

        messages = [system_prompt]
        # Add history if needed, but for now let's keep it simple or just take the last few
        for msg in chat_history[-5:]: # Keep last 5 messages for context
            messages.append(msg)
        
        messages.append({"role": "user", "content": user_message})

        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Chat error: {e}")
            return "I'm sorry, I'm having trouble connecting right now. Please try again later!"