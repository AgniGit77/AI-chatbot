"""
User profile and preferences routes
"""
from flask import Blueprint, request, jsonify, session
from backend.services.user_service import UserService

bp = Blueprint('user', __name__, url_prefix='/api/user')

user_service = UserService()

@bp.route('/profile', methods=['GET', 'POST'])
def manage_profile():
    """Get or update user profile"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'No active session'}), 401
        
        if request.method == 'GET':
            profile = user_service.get_profile(user_id)
            return jsonify({
                'success': True,
                'profile': profile
            })
        
        elif request.method == 'POST':
            data = request.json
            profile = user_service.update_profile(user_id, data)
            return jsonify({
                'success': True,
                'profile': profile
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/measurements', methods=['GET', 'POST'])
def manage_measurements():
    """Get or update user measurements"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'No active session'}), 401
        
        if request.method == 'GET':
            measurements = user_service.get_measurements(user_id)
            return jsonify({
                'success': True,
                'measurements': measurements
            })
        
        elif request.method == 'POST':
            data = request.json
            measurements = user_service.update_measurements(user_id, data)
            return jsonify({
                'success': True,
                'measurements': measurements,
                'message': 'Measurements updated successfully'
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/preferences', methods=['GET', 'POST'])
def manage_preferences():
    """Get or update user style preferences"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'No active session'}), 401
        
        if request.method == 'GET':
            preferences = user_service.get_preferences(user_id)
            return jsonify({
                'success': True,
                'preferences': preferences
            })
        
        elif request.method == 'POST':
            data = request.json
            preferences = user_service.update_preferences(user_id, data)
            return jsonify({
                'success': True,
                'preferences': preferences
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/saved-outfits', methods=['GET', 'POST', 'DELETE'])
def manage_saved_outfits():
    """Manage saved outfit combinations"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'No active session'}), 401
        
        if request.method == 'GET':
            outfits = user_service.get_saved_outfits(user_id)
            return jsonify({
                'success': True,
                'outfits': outfits
            })
        
        elif request.method == 'POST':
            data = request.json
            outfit = user_service.save_outfit(user_id, data)
            return jsonify({
                'success': True,
                'outfit': outfit,
                'message': 'Outfit saved successfully'
            })
        
        elif request.method == 'DELETE':
            outfit_id = request.args.get('id')
            user_service.delete_outfit(user_id, outfit_id)
            return jsonify({
                'success': True,
                'message': 'Outfit deleted successfully'
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
