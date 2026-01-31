"""
User profile and preferences management service
"""
import json
from datetime import datetime
from backend.models.database import get_db, close_db, User, UserMeasurements, SavedOutfits

class UserService:
    """Service for managing user profiles and preferences"""
    
    def get_profile(self, user_id):
        """Get user profile information"""
        db = get_db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if user:
                return {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_anonymous': user.is_anonymous,
                    'created_at': user.created_at.isoformat() if user.created_at else None,
                    'preferences': json.loads(user.preferences) if user.preferences else {}
                }
            
            return None
        finally:
            close_db(db)
    
    def update_profile(self, user_id, data):
        """Update user profile"""
        db = get_db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                # Create new user
                user = User(
                    id=user_id,
                    username=data.get('username'),
                    email=data.get('email'),
                    is_anonymous=data.get('is_anonymous', True)
                )
                db.add(user)
            else:
                # Update existing user
                if 'username' in data:
                    user.username = data['username']
                if 'email' in data:
                    user.email = data['email']
            
            user.last_active = datetime.utcnow()
            db.commit()
            
            return self.get_profile(user_id)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            close_db(db)
    
    def get_measurements(self, user_id):
        """Get user body measurements"""
        db = get_db()
        try:
            measurement = db.query(UserMeasurements).filter(
                UserMeasurements.user_id == user_id
            ).order_by(UserMeasurements.updated_at.desc()).first()
            
            if measurement:
                return {
                    'height_cm': measurement.height_cm,
                    'weight_kg': measurement.weight_kg,
                    'chest_cm': measurement.chest_cm,
                    'waist_cm': measurement.waist_cm,
                    'hip_cm': measurement.hip_cm,
                    'shoulder_width_cm': measurement.shoulder_width_cm,
                    'body_type': measurement.body_type,
                    'size_preference': measurement.size_preference,
                    'updated_at': measurement.updated_at.isoformat()
                }
            
            return None
        finally:
            close_db(db)
    
    def update_measurements(self, user_id, data):
        """Update user measurements"""
        db = get_db()
        try:
            measurement = db.query(UserMeasurements).filter(
                UserMeasurements.user_id == user_id
            ).first()
            
            if not measurement:
                measurement = UserMeasurements(user_id=user_id)
                db.add(measurement)
            
            # Update fields
            if 'height_cm' in data:
                measurement.height_cm = data['height_cm']
            if 'weight_kg' in data:
                measurement.weight_kg = data['weight_kg']
            if 'chest_cm' in data:
                measurement.chest_cm = data['chest_cm']
            if 'waist_cm' in data:
                measurement.waist_cm = data['waist_cm']
            if 'hip_cm' in data:
                measurement.hip_cm = data['hip_cm']
            if 'shoulder_width_cm' in data:
                measurement.shoulder_width_cm = data['shoulder_width_cm']
            if 'body_type' in data:
                measurement.body_type = data['body_type']
            if 'size_preference' in data:
                measurement.size_preference = data['size_preference']
            
            measurement.updated_at = datetime.utcnow()
            db.commit()
            
            return self.get_measurements(user_id)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            close_db(db)
    
    def get_preferences(self, user_id):
        """Get user style preferences"""
        db = get_db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if user and user.preferences:
                return json.loads(user.preferences)
            
            return {
                'style': [],
                'colors': [],
                'brands': [],
                'price_range': {'min': 0, 'max': 1000},
                'occasions': []
            }
        finally:
            close_db(db)
    
    def update_preferences(self, user_id, preferences):
        """Update user style preferences"""
        db = get_db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                user = User(
                    id=user_id,
                    is_anonymous=True,
                    preferences=json.dumps(preferences)
                )
                db.add(user)
            else:
                user.preferences = json.dumps(preferences)
            
            db.commit()
            
            return preferences
        except Exception as e:
            db.rollback()
            raise e
        finally:
            close_db(db)
    
    def get_saved_outfits(self, user_id):
        """Get user's saved outfits"""
        db = get_db()
        try:
            outfits = db.query(SavedOutfits).filter(
                SavedOutfits.user_id == user_id
            ).order_by(SavedOutfits.created_at.desc()).all()
            
            return [{
                'id': outfit.id,
                'name': outfit.outfit_name,
                'items': json.loads(outfit.items) if outfit.items else [],
                'occasion': outfit.occasion,
                'notes': outfit.notes,
                'created_at': outfit.created_at.isoformat()
            } for outfit in outfits]
        finally:
            close_db(db)
    
    def save_outfit(self, user_id, outfit_data):
        """Save a new outfit combination"""
        db = get_db()
        try:
            outfit = SavedOutfits(
                user_id=user_id,
                outfit_name=outfit_data.get('name'),
                items=json.dumps(outfit_data.get('items', [])),
                occasion=outfit_data.get('occasion'),
                notes=outfit_data.get('notes')
            )
            db.add(outfit)
            db.commit()
            
            return {
                'id': outfit.id,
                'name': outfit.outfit_name,
                'items': json.loads(outfit.items),
                'occasion': outfit.occasion,
                'notes': outfit.notes,
                'created_at': outfit.created_at.isoformat()
            }
        except Exception as e:
            db.rollback()
            raise e
        finally:
            close_db(db)
    
    def delete_outfit(self, user_id, outfit_id):
        """Delete a saved outfit"""
        db = get_db()
        try:
            outfit = db.query(SavedOutfits).filter(
                SavedOutfits.id == outfit_id,
                SavedOutfits.user_id == user_id
            ).first()
            
            if outfit:
                db.delete(outfit)
                db.commit()
                return True
            
            return False
        except Exception as e:
            db.rollback()
            raise e
        finally:
            close_db(db)
