"""
Chatbot service for processing user messages and providing fashion advice
"""
import os
import json
from datetime import datetime
from backend.models.database import get_db, close_db, ChatHistory

class ChatbotService:
    """Service for handling chatbot interactions"""
    
    def __init__(self):
        self.context_window = []
        self.max_context = 10
    
    def process_message(self, message, user_id, session_id, context=None):
        """
        Process incoming user message and generate response
        
        Args:
            message: User's message text
            user_id: User identifier
            session_id: Chat session identifier
            context: Additional context data
            
        Returns:
            dict: Response with message, suggestions, and actions
        """
        # Store user message in database
        self._save_message(user_id, session_id, 'user', message)
        
        # Determine intent
        intent = self._analyze_intent(message)
        
        # Generate response based on intent
        response = self._generate_response(intent, message, user_id, context)
        
        # Store bot response
        self._save_message(user_id, session_id, 'bot', response['message'], 
                          json.dumps(response.get('metadata', {})))
        
        return response
    
    def _analyze_intent(self, message):
        """Analyze user message to determine intent"""
        message_lower = message.lower()
        
        # Try-on related intents
        if any(word in message_lower for word in ['try on', 'tryon', 'how does', 'look on me', 'wear']):
            return 'virtual_tryon'
        
        # Size recommendation intents
        if any(word in message_lower for word in ['size', 'fit', 'measurement', 'too big', 'too small']):
            return 'size_recommendation'
        
        # Styling advice intents
        if any(word in message_lower for word in ['style', 'wear with', 'match', 'combine', 'outfit']):
            return 'styling_advice'
        
        # Product search intents
        if any(word in message_lower for word in ['find', 'search', 'looking for', 'similar', 'alternative']):
            return 'product_search'
        
        # Occasion-based intents
        if any(word in message_lower for word in ['wedding', 'work', 'casual', 'formal', 'party', 'date']):
            return 'occasion_styling'
        
        # Help or general query
        return 'general_query'
    
    def _generate_response(self, intent, message, user_id, context):
        """Generate appropriate response based on intent"""
        
        if intent == 'virtual_tryon':
            return {
                'message': "I'd love to help you virtually try on clothes! Please share the product URL from any online store, or upload a photo of the item you'd like to try on. If you haven't uploaded your photo yet, you can do that too!",
                'suggestions': [
                    'Upload my photo',
                    'Paste product URL',
                    'Show me how it works'
                ],
                'action': 'request_tryon_input',
                'metadata': {'intent': intent}
            }
        
        elif intent == 'size_recommendation':
            return {
                'message': "I can help you find the perfect size! To give you accurate recommendations, I'll need your measurements. Would you like to enter them now, or would you prefer to upload a photo for automatic measurement analysis?",
                'suggestions': [
                    'Enter measurements manually',
                    'Upload photo for analysis',
                    'View measurement guide'
                ],
                'action': 'request_measurements',
                'metadata': {'intent': intent}
            }
        
        elif intent == 'styling_advice':
            return {
                'message': "I'd be happy to provide styling advice! Tell me about the item you want to style, or share a product link. I can suggest what to wear it with, how to accessorize, and what occasions it's perfect for.",
                'suggestions': [
                    'I have a specific item',
                    'Need outfit ideas',
                    'Accessory recommendations'
                ],
                'action': 'styling_consultation',
                'metadata': {'intent': intent}
            }
        
        elif intent == 'product_search':
            return {
                'message': "I can help you find the perfect items! What type of clothing are you looking for? I can search across multiple stores and find options that match your style and body type.",
                'suggestions': [
                    'Tops & shirts',
                    'Bottoms & pants',
                    'Dresses & skirts',
                    'Outerwear'
                ],
                'action': 'product_search',
                'metadata': {'intent': intent}
            }
        
        elif intent == 'occasion_styling':
            return {
                'message': "Let me help you dress for the occasion! Tell me more about the event - what's the dress code, what's your style preference, and what's the weather like?",
                'suggestions': [
                    'Formal event',
                    'Casual outing',
                    'Work/professional',
                    'Special occasion'
                ],
                'action': 'occasion_styling',
                'metadata': {'intent': intent}
            }
        
        else:  # general_query
            return {
                'message': """Welcome to your AI Fashion Assistant! 👗✨

I can help you with:
• Virtual try-ons - See how clothes look on you
• Size recommendations - Get the perfect fit
• Styling advice - Complete outfit suggestions
• Product search - Find similar items
• Occasion styling - Dress for any event

What would you like to explore today?""",
                'suggestions': [
                    'Try on clothes virtually',
                    'Get size recommendations',
                    'Find styling ideas',
                    'Search for products'
                ],
                'action': 'show_menu',
                'metadata': {'intent': intent}
            }
    
    def get_chat_history(self, user_id, session_id, limit=50):
        """Retrieve chat history for a user session"""
        db = get_db()
        try:
            query = db.query(ChatHistory).filter(
                ChatHistory.user_id == user_id,
                ChatHistory.session_id == session_id
            ).order_by(ChatHistory.created_at.desc()).limit(limit)
            
            history = []
            for record in query:
                history.append({
                    'type': record.message_type,
                    'message': record.message,
                    'timestamp': record.created_at.isoformat(),
                    'metadata': json.loads(record.message_metadata) if record.message_metadata else {}
                })
            
            return list(reversed(history))
        finally:
            close_db(db)
    
    def _save_message(self, user_id, session_id, message_type, message, metadata=None):
        """Save message to database"""
        db = get_db()
        try:
            chat_record = ChatHistory(
                user_id=user_id,
                session_id=session_id,
                message_type=message_type,
                message=message,
                message_metadata=metadata
            )
            db.add(chat_record)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error saving message: {e}")
        finally:
            close_db(db)
