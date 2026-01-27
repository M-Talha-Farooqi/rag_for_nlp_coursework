import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load your API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env")
    exit()

print(f"🔑 Key found: {api_key[:5]}... (hidden)")

# 2. Configure Google Driver
try:
    genai.configure(api_key=api_key)
    
    print("\n🔍 Scanning for available models...")
    available_models = []
    
    # 3. List all models available to YOUR key
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"   ✅ Found: {m.name}")
            available_models.append(m.name)
            
    if not available_models:
        print("\n❌ No models found! Your API Key might be restricted or invalid.")
    else:
        print(f"\n🚀 Attempting connection with: {available_models[0]}...")
        model = genai.GenerativeModel(available_models[0])
        response = model.generate_content("Hello, are you working?")
        print(f"🎉 Success! Response: {response.text}")

except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {str(e)}")