from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from utils import analyze_skin_tone
from groq_client import GroqService
import os
from dotenv import load_dotenv
import uuid
import traceback

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except Exception as e:
        print(f"Could not create upload folder (standard for serverless): {e}")

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

groq_service = GroqService()

# For Vercel, the app must be accessible at the top level
# app = app 

# Define handlers for Vercel Serverless Functions
def handler(event, context):
    return app(event, context)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        print("=" * 50)
        print("Analyzing request...")
        
        if 'file' not in request.files:
            print("No file provided in request")
            return jsonify({'success': False, 'message': 'No file provided'}), 400
        
        file = request.files['file']
        gender = request.form.get('gender', 'Female')
        style_preference = request.form.get('style_preference', '')
        
        print(f"File received: {file.filename}")
        print(f"Gender: {gender}")
        print(f"Style Preference: {style_preference}")
        
        if file.filename == '':
            print("File has empty filename")
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            print(f"Invalid file type: {file.filename}")
            return jsonify({'success': False, 'message': 'Invalid file type. Please upload JPG or PNG'}), 400
        
        # Check if API key is available from environment
        env_api_key = os.getenv("GROQ_API_KEY")
        if not env_api_key:
            print("GROQ_API_KEY not found in .env")
            return jsonify({'success': False, 'message': 'Groq API Key is not configured. Please set GROQ_API_KEY in .env file.'}), 400
        
        print("API Key configured")
        
        # Analyze skin tone
        print("Starting skin tone analysis...")
        
        # Seek to beginning just in case
        file.seek(0)
        
        # In serverless environments, we handle the file in memory or use /tmp
        # For Vercel, we can try to pass the file pointer directly first,
        # but if that fails, we use a temporary path.
        try:
            # First try direct file pointer (standard Flask)
            analysis_result = analyze_skin_tone(file)
        except Exception as e:
            print(f"Direct file analysis failed: {str(e)}. Trying /tmp...")
            file.seek(0)
            temp_path = os.path.join('/tmp', secure_filename(file.filename))
            file.save(temp_path)
            analysis_result = analyze_skin_tone(temp_path)
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        print(f"Analysis result: {analysis_result}")
        
        if not analysis_result['success']:
            print(f"Analysis failed: {analysis_result['message']}")
            return jsonify(analysis_result), 400
        
        print(f"Skin tone detected: {analysis_result['skin_tone']}")
        print(f"Face shape detected: {analysis_result.get('face_shape', 'Oval')}")
        
        # Get recommendations from Groq
        try:
            print("Calling Groq API for recommendations...")
            groq_response = groq_service.get_fashion_recommendations(
                analysis_result['skin_tone'],
                gender,
                analysis_result.get('face_shape', 'Oval'),
                style_preference
            )
            
            if isinstance(groq_response, dict) and groq_response.get('success') is False:
                return jsonify(groq_response), 500

            print("Recommendations generated successfully")
            
            r, g, b = analysis_result['average_color']
            
            return jsonify({
                'success': True,
                'skin_tone': analysis_result['skin_tone'],
                'face_shape': analysis_result.get('face_shape', 'Oval'),
                'average_color': f'rgb({r},{g},{b})',
                'gender': gender,
                'recommendations': groq_response
            })
        except Exception as e:
            print(f"Error calling Groq API: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                'success': False,
                'message': f'Error generating recommendations: {str(e)}'
            }), 500
    
    except Exception as e:
        print(f"Server error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        chat_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'success': False, 'message': 'No message provided'}), 400
            
        response = groq_service.get_chat_response(user_message, chat_history)
        
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        print(f"Chat route error: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("Starting StyleAI Flask Server...")
    print(f"API Key configured: {bool(os.getenv('GROQ_API_KEY'))}")
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
