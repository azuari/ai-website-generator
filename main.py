from xml.parsers.expat import model

from click import prompt
from flask import Flask, render_template, request, Response
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# configure Gemini API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))    
model = genai.GenerativeModel('gemini-2.5-flash')

generated_code = ""
last_prompt = ""

def generate_website_code(prompt):
    
    enhanced_prompt = f"""
    Create a complete, modern and responsive single HTML file for: {prompt}

    Requirements:
    1. All CSS must be in <style> tag within the HTML
    2. All JavaScript must be in <script> tag within the HTML
    3. Use modern CSS (Flexbox/Grid, animations, gradients)
    4. Make it fully responsive (mobile-friendly)
    5. Include beautiful color schemes and typography
    6. Add smooth animations and transitions
    7. Make it professional and visually appealing
    8. Include relevant content (you can use placeholder text/images)

    Return ONLY the complete HTML code, nothing else. No explanations, no markdown code blocks.
    Start directly with the <!DOCTYPE html>
    """
    try:
        response = model.generate_content(enhanced_prompt)
        code = response.text
        code = code.replace('```html','').replace('```','').strip()
        return code
         
    except Exception as e:
        return f"<html><h1>Error: {str(e)}</h1></html>"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    global generated_code, last_prompt
    prompt = request.form.get('prompt', '').strip()

    if not prompt:
        return render_template('index.html', error="please enter a prompt")

    last_prompt = prompt
    generated_code = generate_website_code(prompt)
    return render_template('result.html', prompt=last_prompt)

@app.route('/preview')
def preview():
    return generated_code

@app.route('/download')
def download():
    return Response(
        generated_code,
        mimetype='text/html',
        headers={'Content-Disposition': 'attachment; filename=generated_website.html'}
    )

@app.route('/get-code')
def get_code():
    return generated_code, 200, {'Content-Type': 'text/plain'}

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)