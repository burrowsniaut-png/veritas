from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime
from ai_detector_pro import scrape_website, analyze_with_gemini

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Simple "database" - in production use real database
users = {}
results = {}

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return 'Invalid login'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    urls = request.form.get('urls', '').strip().split('\n')
    urls = [url.strip() for url in urls if url.strip()][:25]
    
    if not urls:
        return "No URLs provided"
    
    try:
        # Process URLs one by one with delay to prevent Ollama timeout
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
                # 3 second delay between URLs to prevent Ollama timeout
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
                output += f"<p style='color:red'>Error: {result.get('error', 'Unknown error')}</p>"
            output += "<hr>"
        
        output += "<br><a href='/dashboard'>Back to Dashboard</a>"
        return output
        
    except Exception as e:
        return f"Error running analysis: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)