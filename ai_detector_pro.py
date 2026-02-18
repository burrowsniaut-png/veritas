import requests
from playwright.sync_api import sync_playwright
import time
import json
from openai import OpenAI

def scrape_website(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, timeout=60000)
        text = page.inner_text('body')[:3000]
        browser.close()
        return text

def analyze_with_deepseek(text):
    # Use OpenRouter API
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    
    prompt = f"""Analyze this text and determine if it was written by a human or AI.
    Provide a detailed analysis including:
    - Human vs AI probability estimate
    - Specific indicators you noticed
    - Confidence level
    
    Text to analyze:
    {text[:2000]}"""
    
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.2-3b-instruct:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Analysis error: {str(e)}"

# Get URLs (max 25)
results = []
for i, url in enumerate(url_list, 1):
    print(f"\n{'='*60}")
    print(f"[{i}/{len(url_list)}] {url}")
    print(f"{'='*60}")
    
    try:
        text = scrape_website(url)
        print(f"Scraped {len(text)} chars")
        
        print("Analyzing...")
        result = analyze_with_deepseek(text)
        
        print(f"\nVERITAS ANALYSIS:")
        print(result)
        print(f"{'='*60}\n")
        
        results.append({"url": url, "analysis": result, "status": "ok"})
        
        with open('veritas_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        if i < len(url_list):
            print("Cooling down (3s)...")
            time.sleep(3)
            
    except Exception as e:
        print(f"\nFAILED: {e}")
        results.append({"url": url, "error": str(e), "status": "fail"})
        with open('veritas_results.json', 'w') as f:
            json.dump(results, f, indent=2)
