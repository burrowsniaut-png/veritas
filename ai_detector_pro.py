import requests
from playwright.sync_api import sync_playwright
import time
import json
from google import genai
import os

def scrape_website(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, timeout=60000)
        text = page.inner_text('body')[:3000]
        browser.close()
        return text

# Configure Gemini with API key from environment variable
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

def analyze_with_gemini(text):
    try:
        # Debug: Check if API key is set
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return "Error: GEMINI_API_KEY not found in environment variables"
        
        prompt = f"""Analyze this text and determine if it was written by a human or AI.

Provide a detailed analysis including:
- Human vs AI probability estimate
- Specific indicators you noticed
- Confidence level

Text to analyze:
{text[:3000]}"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error analyzing text: {str(e)}"

def analyze_multiple_urls(urls):
    results = []
    for url in urls:
        try:
            print(f"Processing: {url}")
            content = scrape_website(url)
            
            if content.startswith("Error"):
                results.append({
                    'url': url,
                    'status': 'error',
                    'analysis': content
                })
            else:
                analysis = analyze_with_gemini(content)
                results.append({
                    'url': url,
                    'status': 'success',
                    'analysis': analysis
                })
            
            # Small delay to be nice to servers
            time.sleep(2)
            
        except Exception as e:
            results.append({
                'url': url,
                'status': 'error',
                'analysis': f"Error: {str(e)}"
            })
    
    return results
