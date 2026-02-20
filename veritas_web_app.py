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
    urls = request.form.get('urls', '').strip().split('\n')
    urls = [url.strip() for url in urls if url.strip()][:25]
    
    if not urls:
        return "No URLs provided"
    
    try:
        results_list = []
        for url in urls:
            try:
                content = scrape_website(url)
                
                if content.startswith("Error"):
                    results_list.append({
                        'url': url,
                        'status': 'error',
                        'analysis': content
                    })
                else:
                    analysis = analyze_with_gemini(content)
                    results_list.append({
                        'url': url,
                        'status': 'ok',
                        'analysis': analysis
                    })
                
                import time
                time.sleep(3)
                
            except Exception as e:
                results_list.append({
                    'url': url,
                    'status': 'error',
                    'analysis': f"Analysis failed: {str(e)}"
                })
        
        results[session['username']] = {
            'urls': urls,
            'results': results_list,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'completed'
        }
        
        output = "<h2>Analysis Results</h2>"
        for result in results_list:
            output += f"<h3>{result['url']}</h3>"
            if result['status'] == 'ok':
                output += f"<p>{result['analysis']}</p>"
            else:
                output += f"<p style='color:red'>Error: {result['analysis']}</p>"
            output += "<hr>"
        
        output += "<br><a href='/dashboard'>Back to Dashboard</a>"
        return output
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"<h2>Error running analysis</h2><p style='color:red'>{str(e)}</p><pre>{error_details}</pre><br><a href='/dashboard'>Back to Dashboard</a>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
