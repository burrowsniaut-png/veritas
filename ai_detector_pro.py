import requests
from playwright.sync_api import sync_playwright
import time
import json
import google.generativeai as genai
import os

def scrape_website(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, timeout=60000)
        text = page.inner_text('body')[:3000]
        browser.close()
        return text

import requests

import google.generativeai as genai
import os

# Configure Gemini with API key from environment variable
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

def analyze_with_gemini(text):
    try:
        # Debug: Check if API key is set
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return "Error: GEMINI_API_KEY not found in environment variables"
        
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""Analyze this text and determine if it was written by AI or a human.
        
Provide a detailed analysis including:
- Human vs AI probability estimate
- Specific indicators you noticed
- Confidence level

Text to analyze:
{text[:3000]}"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Return the actual error message
        return f"Analysis error: {str(e)}"
    
    for i, url in enumerate(url_list, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{len(url_list)}] {url}")
        print(f"{'='*60}")
        
        try:
            text = scrape_website(url)
            print(f"Scraped {len(text)} chars")
            
            print("Analyzing (up to 10 minutes)...")
            result = analyze_with_gemini(text)
            
            print(f"\nVERITAS ANALYSIS:")
            print(result)
            print(f"{'='*60}\n")
            
            results.append({"url": url, "analysis": result, "status": "ok"})
            
            with open('veritas_results.json', 'w') as f:
                json.dump(results, f, indent=2)
            
            if i < len(url_list):
                print("Cooling down (5s)...")
                time.sleep(5)
                
        except Exception as e:
            print(f"\nFAILED: {e}")
            results.append({"url": url, "error": str(e), "status": "fail"})
            with open('veritas_results.json', 'w') as f:
                json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"DONE. {len([r for r in results if r['status']=='ok'])} succeeded.")
    print(f"{'='*60}")
    
    return results

# Only run interactive mode if called directly (not imported)
if __name__ == "__main__":
    # Get URLs (max 25)
    urls = []
    print("Enter URLs (one per line). Type 'done' when finished. Max 25:")
    while len(urls) < 25:
        url = input("URL: ").strip()
        if url.lower() == 'done':
            break
        if url:
            if not url.startswith('http'):
                url = 'https://' + url
            urls.append(url)
    
    if urls:
        analyze_urls(urls)
=======
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



>>>>>>> abdb0e55ebc00c95eb3a1e964f7ac92e5ba94369
