import os
from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from datetime import datetime
import json
from ai_detector_pro import scrape_website, analyze_with_gemini

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Simple in-memory storage (replace with database in production)
users = {}
results = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            return "Username already exists"
        
        users[username] = password
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        
        return "Invalid credentials"
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=session['username'])

@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    # DEBUG LOGGING AT THE VERY START
    print(f"DEBUG: Analyze function started")
    print(f"DEBUG: User: {session.get('username')}")
    print(f"DEBUG: Form data: {dict(request.form)}")
    
    try:
        urls = request.form.get('urls', '').strip().split('\n')
        urls = [url.strip() for url in urls if url.strip()][:25]
        
        print(f"DEBUG: Parsed URLs: {urls}")
        
        if not urls:
            print("DEBUG: No URLs provided")
            return "No URLs provided"
        
        results_list = []
        
        for url in urls:
            print(f"DEBUG: Processing URL: {url}")
            
            try:
                print(f"DEBUG: About to scrape: {url}")
                content = scrape_website(url)
                print(f"DEBUG: Scrape result: {content[:100] if content else 'EMPTY'}")
                
                if content.startswith("Error"):
                    print(f"DEBUG: Scrape error detected")
                    results_list.append({
                        'url': url,
                        'status': 'error',
                        'analysis': content
