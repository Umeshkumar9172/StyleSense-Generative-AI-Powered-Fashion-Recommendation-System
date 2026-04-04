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

    def get_fashion_recommendations(self, skin_tone, gender, face_shape="Oval", style_preference=""):
        if not self.client:
            print("Error: Groq client not initialized")
            return {"success": False, "message": "Groq API Key is missing."}

        print(f"\nGenerating advanced recommendations for: {gender} with {skin_tone} skin tone, {face_shape} face shape and {style_preference if style_preference else 'Default'} style")

        system_prompt = f"""
You are an advanced AI Fashion Stylist and Shopping Recommendation Engine. 
  
 ----------------------------------- 
 🧠 INPUT: 
 - Gender: {gender} 
 - Skin Tone: {skin_tone} 
 - Face Shape: {face_shape} 
 - Preferred Style: {style_preference if style_preference else ""} (optional) 
  
 ----------------------------------- 
 🎯 OBJECTIVE: 
 Generate personalized fashion recommendations based on all inputs. 
  
 ----------------------------------- 
 🚨 STYLE HANDLING RULES: 
  
 IF Preferred Style is PROVIDED: 
 - STRICTLY follow that style in ALL outfit recommendations 
  
 IF Preferred Style is EMPTY: 
 - Default to "Smart Casual" 
  
 ----------------------------------- 
 🎨 STYLE DEFINITIONS: 
  
 - Casual → relaxed, comfortable (t-shirts, jeans, sneakers) 
 - Formal → clean, structured (blazers, trousers, shirts) 
 - Streetwear → trendy, oversized, bold (hoodies, cargo, sneakers) 
 - Ethnic → traditional (kurti, saree, sherwani) 
 - Minimalist → simple, neutral colors, clean fits 
 - Sporty → athletic wear (joggers, hoodies, trainers) 
 - Party → stylish, bold, statement outfits 
 - Smart Casual → mix of formal + casual (shirts + jeans, blazers + t-shirt) 
  
 ----------------------------------- 
 🚨 STRICT RULES: 
  
 1. Gender-Specific: 
    - Female → saree, kurti, dresses, heels, handbags 
    - Male → shirts, jeans, sneakers, watches 
  
 2. Style MUST influence: 
    - Outfit type 
    - Color choices 
    - Accessories 
  
 3. Keep recommendations REALISTIC & TRENDY 
  
 ----------------------------------- 
 🛒 SHOPPING RULES: 
  
 Use ONLY: 
 - Amazon 
 - Flipkart 
 - Myntra 
 - Ajio 
  
 Generate SEARCH LINKS: 
  
 Amazon: 
 `https://www.amazon.in/s?k={{query}}`  
  
 Flipkart: 
 `https://www.flipkart.com/search?q={{query}}`  
  
 Myntra: 
 `https://www.myntra.com/{{query}}`  
  
 Ajio: 
 `https://www.ajio.com/search/?text={{query}}`  
  
 ----------------------------------- 
 📦 OUTPUT FORMAT (STRICT JSON): 
  
 {{ 
   "analysis": {{ 
     "style_summary": "Include style preference in explanation", 
     "detected_style": "{style_preference if style_preference else "Smart Casual"}", 
     "color_recommendation": ["color1", "color2", "color3"], 
     "avoid_colors": ["color1", "color2"] 
   }}, 
  
   "outfits": [ 
     {{ 
       "occasion": "Casual", 
       "style": "{style_preference if style_preference else "Smart Casual"}", 
       "items": [
         {{
           "item_name": "Product Name",
           "category": "Topwear/Bottomwear/Footwear",
           "color": "Color Name",
           "reason": "Why it suits the user",
           "platform": "Amazon/Flipkart/Myntra/Ajio",
           "search_link": "Link here"
         }}
       ] 
     }}, 
     {{ 
       "occasion": "Party", 
       "style": "{style_preference if style_preference else "Smart Casual"}", 
       "items": [
         {{
           "item_name": "Product Name",
           "category": "Topwear/Bottomwear/Footwear",
           "color": "Color Name",
           "reason": "Why it suits the user",
           "platform": "Amazon/Flipkart/Myntra/Ajio",
           "search_link": "Link here"
         }}
       ] 
     }},
     {{ 
       "occasion": "Office", 
       "style": "{style_preference if style_preference else "Smart Casual"}", 
       "items": [
         {{
           "item_name": "Product Name",
           "category": "Topwear/Bottomwear/Footwear",
           "color": "Color Name",
           "reason": "Why it suits the user",
           "platform": "Amazon/Flipkart/Myntra/Ajio",
           "search_link": "Link here"
         }}
       ] 
     }}
   ], 
  
   "accessories": [
     {{
       "item_name": "Accessory Name",
       "reason": "Why it suits the user",
       "platform": "Platform Name",
       "search_link": "Link here"
     }}
   ],

   "styling_tips": [ 
     "Tips aligned with selected style" 
   ] 
 }} 
  
 ----------------------------------- 
 ⚠️ IMPORTANT: 
 - Output ONLY JSON 
 - No extra text
 - Each occasion MUST have at least 2 items in the "items" array.
 - Replace spaces with "+" in query part of search links.
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
                        "content": f"Provide fashion recommendations for a {gender} with {skin_tone} skin tone, {face_shape} face shape, and {style_preference if style_preference else 'Smart Casual'} style preference.",
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