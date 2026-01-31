"""
Privacy and data management service
"""
import json
import os
from datetime import datetime
from backend.models.database import (
    get_db, close_db, User, UserMeasurements, Avatar, 
    ChatHistory, TryOnHistory, SavedOutfits
)

class PrivacyService:
    """Service for managing user privacy and data"""
    
    def export_user_data(self, user_id):
        """
        Export all user data
        
        Args:
            user_id: User identifier
            
        Returns:
            dict: Complete user data export
        """
        db = get_db()
        try:
            # Get profile
            user = db.query(User).filter(User.id == user_id).first()
            profile = {
                'username': user.username if user else None,
                'email': user.email if user else None,
                'created_at': user.created_at.isoformat() if user and user.created_at else None,
                'preferences': json.loads(user.preferences) if user and user.preferences else {}
            }
            
            # Get measurements
            measurements = db.query(UserMeasurements).filter(
                UserMeasurements.user_id == user_id
            ).all()
            measurements_data = [{
                'height_cm': m.height_cm,
                'weight_kg': m.weight_kg,
                'chest_cm': m.chest_cm,
                'waist_cm': m.waist_cm,
                'hip_cm': m.hip_cm,
                'shoulder_width_cm': m.shoulder_width_cm,
                'body_type': m.body_type,
                'updated_at': m.updated_at.isoformat()
            } for m in measurements]
            
            # Get chat history
            chats = db.query(ChatHistory).filter(
                ChatHistory.user_id == user_id
            ).all()
            chat_data = [{
                'type': c.message_type,
                'message': c.message,
                'timestamp': c.created_at.isoformat()
            } for c in chats]
            
            # Get try-on history
            tryons = db.query(TryOnHistory).filter(
                TryOnHistory.user_id == user_id
            ).all()
            tryon_data = [{
                'product_url': t.product_url,
                'product_name': t.product_name,
                'rating': t.rating,
                'date': t.created_at.isoformat()
            } for t in tryons]
            
            # Get saved outfits
            outfits = db.query(SavedOutfits).filter(
                SavedOutfits.user_id == user_id
            ).all()
            outfit_data = [{
                'name': o.outfit_name,
                'items': json.loads(o.items) if o.items else [],
                'occasion': o.occasion,
                'notes': o.notes,
                'created_at': o.created_at.isoformat()
            } for o in outfits]
            
            return {
                'export_date': datetime.utcnow().isoformat(),
                'user_id': user_id,
                'profile': profile,
                'measurements': measurements_data,
                'chat_history': chat_data,
                'tryon_history': tryon_data,
                'saved_outfits': outfit_data
            }
        finally:
            close_db(db)
    
    def delete_user_data(self, user_id, data_type='all'):
        """
        Delete user data based on type
        
        Args:
            user_id: User identifier
            data_type: Type of data to delete ('all', 'images', 'measurements', 'history', 'chats', 'outfits')
        """
        db = get_db()
        try:
            if data_type == 'all':
                # Delete all user data
                db.query(UserMeasurements).filter(UserMeasurements.user_id == user_id).delete()
                db.query(Avatar).filter(Avatar.user_id == user_id).delete()
                db.query(ChatHistory).filter(ChatHistory.user_id == user_id).delete()
                db.query(TryOnHistory).filter(TryOnHistory.user_id == user_id).delete()
                db.query(SavedOutfits).filter(SavedOutfits.user_id == user_id).delete()
                db.query(User).filter(User.id == user_id).delete()
                
            elif data_type == 'images':
                # Delete avatars and try-on images
                avatars = db.query(Avatar).filter(Avatar.user_id == user_id).all()
                for avatar in avatars:
                    if avatar.image_path and os.path.exists(avatar.image_path):
                        os.remove(avatar.image_path)
                db.query(Avatar).filter(Avatar.user_id == user_id).delete()
                
                tryons = db.query(TryOnHistory).filter(TryOnHistory.user_id == user_id).all()
                for tryon in tryons:
                    if tryon.result_image_path and os.path.exists(tryon.result_image_path):
                        os.remove(tryon.result_image_path)
                db.query(TryOnHistory).filter(TryOnHistory.user_id == user_id).delete()
                
            elif data_type == 'measurements':
                db.query(UserMeasurements).filter(UserMeasurements.user_id == user_id).delete()
                
            elif data_type == 'history':
                db.query(TryOnHistory).filter(TryOnHistory.user_id == user_id).delete()
                
            elif data_type == 'chats':
                db.query(ChatHistory).filter(ChatHistory.user_id == user_id).delete()
                
            elif data_type == 'outfits':
                db.query(SavedOutfits).filter(SavedOutfits.user_id == user_id).delete()
            
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            close_db(db)
    
    def update_consent(self, user_id, consent_type, granted):
        """
        Update user consent preferences
        
        Args:
            user_id: User identifier
            consent_type: Type of consent
            granted: Whether consent is granted
        """
        db = get_db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if user:
                preferences = json.loads(user.preferences) if user.preferences else {}
                if 'consent' not in preferences:
                    preferences['consent'] = {}
                
                preferences['consent'][consent_type] = {
                    'granted': granted,
                    'updated_at': datetime.utcnow().isoformat()
                }
                
                user.preferences = json.dumps(preferences)
                db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            close_db(db)
    
    def anonymize_user_data(self, user_id):
        """
        Anonymize user data while retaining aggregate statistics
        
        Args:
            user_id: User identifier
        """
        db = get_db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if user:
                user.username = None
                user.email = None
                user.is_anonymous = True
                user.preferences = None
                db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            close_db(db)
