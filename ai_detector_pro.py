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

def analyze_with_deepseek(text):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.2:1b",
        "prompt": f"Analyze this text and determine if it was written by a human or AI. Provide detailed analysis. Text: {text[:2000]}", 
        "stream": False
    }
    try:
        response = requests.post(url, json=data, timeout=300)
        return response.json()['response']
    except Exception as e:
        return f"Analysis error: {str(e)}"
        
            
           



