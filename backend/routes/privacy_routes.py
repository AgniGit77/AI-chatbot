"""
Privacy and data management routes
"""
from flask import Blueprint, request, jsonify, session
from backend.services.privacy_service import PrivacyService

bp = Blueprint('privacy', __name__, url_prefix='/api/privacy')

privacy_service = PrivacyService()

@bp.route('/export-data', methods=['GET'])
def export_data():
    """Export all user data"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'No active session'}), 401
        
        data = privacy_service.export_user_data(user_id)
        
        return jsonify({
            'success': True,
            'data': data,
            'message': 'Data exported successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/delete-data', methods=['POST'])
def delete_data():
    """Delete specific user data"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'No active session'}), 401
        
        data = request.json
        data_type = data.get('data_type')  # 'all', 'images', 'measurements', 'history'
        
        privacy_service.delete_user_data(user_id, data_type)
        
        if data_type == 'all':
            session.clear()
        
        return jsonify({
            'success': True,
            'message': f'{data_type.title()} data deleted successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/policy', methods=['GET'])
def get_privacy_policy():
    """Get privacy policy information"""
    policy = {
        'last_updated': '2024-01-31',
        'data_retention_days': 365,
        'data_collected': [
            'Body measurements (encrypted)',
            'Style preferences',
            'Chat history',
            'Virtual try-on results',
            'Saved outfits'
        ],
        'data_sharing': 'We do not share your data with third parties without explicit consent',
        'encryption': 'All sensitive data is encrypted at rest and in transit',
        'anonymous_mode': 'Available - no personal information required',
        'data_deletion': 'You can delete your data at any time',
        'contact': 'privacy@fashionchatbot.example.com'
    }
    
    return jsonify({
        'success': True,
        'policy': policy
    })

@bp.route('/consent', methods=['POST'])
def manage_consent():
    """Manage user consent preferences"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'No active session'}), 401
        
        data = request.json
        consent_type = data.get('consent_type')
        granted = data.get('granted', False)
        
        privacy_service.update_consent(user_id, consent_type, granted)
        
        return jsonify({
            'success': True,
            'message': 'Consent preferences updated'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
