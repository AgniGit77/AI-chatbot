"""
Virtual try-on routes
"""
from flask import Blueprint, request, jsonify, session, send_file
from werkzeug.utils import secure_filename
from backend.services.tryon_service import TryOnService
from backend.utils.file_handler import FileHandler
import os

bp = Blueprint('tryon', __name__, url_prefix='/api/tryon')

tryon_service = TryOnService()
file_handler = FileHandler()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload-image', methods=['POST'])
def upload_image():
    """Upload user image for virtual try-on"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'No active session'}), 401
        
        # Save file securely
        file_path = file_handler.save_user_image(file, user_id)
        
        return jsonify({
            'success': True,
            'file_path': file_path,
            'message': 'Image uploaded successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/process', methods=['POST'])
def process_tryon():
    """Process virtual try-on request"""
    try:
        data = request.json
        product_url = data.get('product_url')
        user_image_path = data.get('user_image_path')
        user_id = session.get('user_id')
        
        if not product_url:
            return jsonify({'success': False, 'error': 'Product URL required'}), 400
        
        # Process virtual try-on
        result = tryon_service.process_tryon(
            product_url=product_url,
            user_image_path=user_image_path,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'result_image': result['image_path'],
            'fit_analysis': result['fit_analysis'],
            'size_recommendation': result['size_recommendation'],
            'styling_tips': result['styling_tips']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/analyze-fit', methods=['POST'])
def analyze_fit():
    """Analyze fit based on user measurements"""
    try:
        data = request.json
        product_url = data.get('product_url')
        user_id = session.get('user_id')
        
        analysis = tryon_service.analyze_fit(
            product_url=product_url,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/size-recommendation', methods=['POST'])
def get_size_recommendation():
    """Get size recommendation for a product"""
    try:
        data = request.json
        product_url = data.get('product_url')
        user_id = session.get('user_id')
        
        recommendation = tryon_service.get_size_recommendation(
            product_url=product_url,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'recommendation': recommendation
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/history', methods=['GET'])
def get_tryon_history():
    """Get user's try-on history"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'No active session'}), 401
        
        history = tryon_service.get_user_history(user_id)
        
        return jsonify({
            'success': True,
            'history': history
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
