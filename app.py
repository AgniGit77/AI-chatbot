"""
AI Fashion Chatbot - Main Application Entry Point
"""
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
from backend.routes import chat_routes, tryon_routes, user_routes, privacy_routes
from backend.models.database import init_db

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')

# Configuration
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_UPLOAD_SIZE', 16 * 1024 * 1024))
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')

# Enable CORS
CORS(app, supports_credentials=True)

# Initialize database
init_db()

# Register blueprints
app.register_blueprint(chat_routes.bp)
app.register_blueprint(tryon_routes.bp)
app.register_blueprint(user_routes.bp)
app.register_blueprint(privacy_routes.bp)

@app.route('/')
def index():
    """Render main chatbot interface"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'AI Fashion Chatbot'})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run the application
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
