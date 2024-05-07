import os
import requests
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS



# Initialize OpenAI client with API Key
api_key = 'api key here'

# Initialize Flask application
app = Flask(__name__)
CORS(app)

@app.route('/generate-content', methods=['POST'])
def generate_content():
    data = request.get_json()
    content_format = data.get('format', 'post')  # Default to 'post' if not provided
    topic = data.get('topic', 'Technology')  # Default to 'Technology' if not provided
    emotion = data.get('emotion', '')  # Default to an empty string if not provided
    length = data.get('length', 150)  # Default to 150 tokens if not provided
    target_audience = data.get('target_audience', 'general public')  # Default to 'general public' if not provided

    # Create a detailed prompt using the provided parameters
    prompt = (f"Write a {content_format} about {topic} for {target_audience} "
              f"that conveys {emotion}. The content should be engaging and approximately {length} words.")
    
    openai.api_key = api_key

    # Generate the marketing content using OpenAI
    try:
        chat_completion = openai.ChatCompletion.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            max_tokens=length,
            temperature = 0.2
        )
        # Extracting the text response from the completion
        generated_text = chat_completion['choices'][0]['message']['content']
        return jsonify({"text": generated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
   
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True, use_reloader=False)  # Run the app
