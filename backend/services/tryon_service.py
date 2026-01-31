"""
Virtual try-on service for processing clothing visualization
"""
import os
import json
from datetime import datetime
from backend.models.database import get_db, close_db, TryOnHistory, UserMeasurements
from backend.services.product_service import ProductService
from backend.utils.image_processor import ImageProcessor

class TryOnService:
    """Service for virtual try-on functionality"""
    
    def __init__(self):
        self.product_service = ProductService()
        self.image_processor = ImageProcessor()
    
    def process_tryon(self, product_url, user_image_path, user_id):
        """
        Process virtual try-on request
        
        Args:
            product_url: URL of the product to try on
            user_image_path: Path to user's image
            user_id: User identifier
            
        Returns:
            dict: Try-on result with image path, fit analysis, and recommendations
        """
        # Fetch product information
        product_info = self.product_service.get_product_info(product_url)
        
        # Get user measurements if available
        measurements = self._get_user_measurements(user_id)
        
        # Simulate virtual try-on (in production, this would use ML models)
        result_image_path = self._simulate_tryon(user_image_path, product_info)
        
        # Analyze fit
        fit_analysis = self.analyze_fit(product_url, user_id, product_info, measurements)
        
        # Get size recommendation
        size_recommendation = self.get_size_recommendation(product_url, user_id, product_info, measurements)
        
        # Generate styling tips
        styling_tips = self._generate_styling_tips(product_info, measurements)
        
        # Save to history
        self._save_tryon_history(user_id, product_url, product_info.get('name'), result_image_path)
        
        return {
            'image_path': result_image_path,
            'fit_analysis': fit_analysis,
            'size_recommendation': size_recommendation,
            'styling_tips': styling_tips,
            'product_info': product_info
        }
    
    def analyze_fit(self, product_url, user_id, product_info=None, measurements=None):
        """Analyze how a garment will fit the user"""
        if not product_info:
            product_info = self.product_service.get_product_info(product_url)
        
        if not measurements:
            measurements = self._get_user_measurements(user_id)
        
        if not measurements:
            return {
                'summary': 'Please provide your measurements for accurate fit analysis',
                'details': [],
                'recommendation': 'Enter measurements for personalized fit advice'
            }
        
        # Simulate fit analysis (in production, use ML models)
        analysis = {
            'summary': 'Based on your measurements, this item should fit well',
            'details': [
                f"Body type: {measurements.get('body_type', 'Not specified')}",
                f"Fit preference: {measurements.get('size_preference', 'regular')}",
                'The garment length appears suitable for your height',
                'Shoulder width matches your measurements'
            ],
            'recommendation': 'True to size',
            'confidence': 0.85
        }
        
        # Add specific advice based on garment type
        garment_type = product_info.get('category', '').lower()
        
        if 'dress' in garment_type or 'top' in garment_type:
            analysis['details'].append('Consider your bust and shoulder measurements for optimal fit')
        elif 'pants' in garment_type or 'jeans' in garment_type:
            analysis['details'].append('Pay attention to waist and hip measurements')
        
        return analysis
    
    def get_size_recommendation(self, product_url, user_id, product_info=None, measurements=None):
        """Get size recommendation for a product"""
        if not product_info:
            product_info = self.product_service.get_product_info(product_url)
        
        if not measurements:
            measurements = self._get_user_measurements(user_id)
        
        if not measurements:
            return {
                'recommended_size': 'Unable to determine',
                'alternative_sizes': [],
                'notes': 'Please provide your measurements for accurate size recommendations',
                'sizing_chart_available': False
            }
        
        # Simulate size recommendation (in production, use ML models)
        recommendation = {
            'recommended_size': 'M',
            'alternative_sizes': ['S', 'L'],
            'notes': [
                'Based on your measurements, size M should fit well',
                'This brand tends to run true to size',
                'For a looser fit, consider size L'
            ],
            'sizing_chart_available': True,
            'size_conversions': {
                'US': 'M (8-10)',
                'UK': 'M (12-14)',
                'EU': 'M (40-42)'
            },
            'confidence': 0.82
        }
        
        # Adjust based on fit preference
        fit_pref = measurements.get('size_preference', 'regular')
        if fit_pref == 'loose':
            recommendation['notes'].append('Since you prefer a loose fit, you might want to go up one size')
        elif fit_pref == 'fitted':
            recommendation['notes'].append('For a fitted look as you prefer, the recommended size is ideal')
        
        return recommendation
    
    def get_user_history(self, user_id):
        """Get user's try-on history"""
        db = get_db()
        try:
            query = db.query(TryOnHistory).filter(
                TryOnHistory.user_id == user_id
            ).order_by(TryOnHistory.created_at.desc()).limit(20)
            
            history = []
            for record in query:
                history.append({
                    'id': record.id,
                    'product_url': record.product_url,
                    'product_name': record.product_name,
                    'result_image': record.result_image_path,
                    'rating': record.rating,
                    'date': record.created_at.isoformat()
                })
            
            return history
        finally:
            close_db(db)
    
    def _get_user_measurements(self, user_id):
        """Get user measurements from database"""
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
                    'size_preference': measurement.size_preference
                }
            return None
        finally:
            close_db(db)
    
    def _simulate_tryon(self, user_image_path, product_info):
        """Simulate virtual try-on (placeholder for ML model)"""
        # In production, this would use ML models for realistic try-on
        # For now, return a placeholder result
        return f"/static/tryon_results/simulated_{datetime.now().timestamp()}.jpg"
    
    def _generate_styling_tips(self, product_info, measurements):
        """Generate styling tips for the garment"""
        tips = [
            f"This {product_info.get('category', 'item')} works great for various occasions",
            "Consider pairing with complementary colors for a cohesive look",
        ]
        
        garment_type = product_info.get('category', '').lower()
        
        if 'dress' in garment_type:
            tips.extend([
                "Add a belt to accentuate your waist",
                "Pair with heels for formal events or sneakers for casual wear"
            ])
        elif 'top' in garment_type or 'shirt' in garment_type:
            tips.extend([
                "Tuck into high-waisted bottoms for a polished look",
                "Layer with a blazer for professional settings"
            ])
        elif 'pants' in garment_type or 'jeans' in garment_type:
            tips.extend([
                "Cuff the hem for a casual, relaxed style",
                "Pair with a fitted top to balance proportions"
            ])
        
        return tips
    
    def _save_tryon_history(self, user_id, product_url, product_name, result_image_path):
        """Save try-on to history"""
        db = get_db()
        try:
            history_record = TryOnHistory(
                user_id=user_id,
                product_url=product_url,
                product_name=product_name,
                result_image_path=result_image_path
            )
            db.add(history_record)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error saving try-on history: {e}")
        finally:
            close_db(db)
