"""
Chat routes for AI fashion chatbot
"""
from flask import Blueprint, request, jsonify, session
from backend.services.chatbot_service import ChatbotService
from backend.services.style_service import StyleService
import uuid

bp = Blueprint('chat', __name__, url_prefix='/api/chat')

chatbot_service = ChatbotService()
style_service = StyleService()

@bp.route('/message', methods=['POST'])
def send_message():
    """Handle incoming chat messages"""
    try:
        data = request.json
        message = data.get('message', '')
        user_id = session.get('user_id')
        session_id = session.get('chat_session_id')
        
        # Create session if doesn't exist
        if not session_id:
            session_id = str(uuid.uuid4())
            session['chat_session_id'] = session_id
        
        if not user_id:
            # Create anonymous user
            user_id = str(uuid.uuid4())
            session['user_id'] = user_id
            session['is_anonymous'] = True
        
        # Process message with chatbot service
        response = chatbot_service.process_message(
            message=message,
            user_id=user_id,
            session_id=session_id,
            context=data.get('context', {})
        )
        
        return jsonify({
            'success': True,
            'response': response['message'],
            'suggestions': response.get('suggestions', []),
            'action': response.get('action'),
            'metadata': response.get('metadata', {})
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/style-advice', methods=['POST'])
def get_style_advice():
    """Get styling advice for a specific item"""
    try:
        data = request.json
        product_url = data.get('product_url')
        user_preferences = data.get('preferences', {})
        user_id = session.get('user_id')
        
        advice = style_service.get_styling_advice(
            product_url=product_url,
            user_id=user_id,
            preferences=user_preferences
        )
        
        return jsonify({
            'success': True,
            'advice': advice
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/outfit-suggestions', methods=['POST'])
def get_outfit_suggestions():
    """Get complete outfit suggestions"""
    try:
        data = request.json
        base_item = data.get('base_item')
        occasion = data.get('occasion')
        user_id = session.get('user_id')
        
        suggestions = style_service.generate_outfit_suggestions(
            base_item=base_item,
            occasion=occasion,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'outfits': suggestions
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/history', methods=['GET'])
def get_chat_history():
    """Get user's chat history"""
    try:
        user_id = session.get('user_id')
        session_id = session.get('chat_session_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'No active session'}), 401
        
        history = chatbot_service.get_chat_history(user_id, session_id)
        
        return jsonify({
            'success': True,
            'history': history
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
