import requests
from playwright.sync_api import sync_playwright
import time
import json

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
        return f"Analysis error: {str(e)}"
    
    for i, url in enumerate(url_list, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{len(url_list)}] {url}")
        print(f"{'='*60}")
        
        try:
            text = scrape_website(url)
            print(f"Scraped {len(text)} chars")
            
            print("Analyzing (up to 10 minutes)...")
            result = analyze_with_deepseek(text)
            
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