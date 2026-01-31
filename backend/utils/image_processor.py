"""
Image processing utilities for virtual try-on
"""
from PIL import Image
import numpy as np
import io
import os

class ImageProcessor:
    """Utility for processing images for virtual try-on"""
    
    def __init__(self):
        self.max_dimension = 2048
        self.target_dimension = 1024
    
    def process_user_image(self, image_path):
        """
        Process user uploaded image for virtual try-on
        
        Args:
            image_path: Path to user image
            
        Returns:
            dict: Processed image data and metadata
        """
        try:
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if too large
            if max(img.size) > self.max_dimension:
                img = self._resize_image(img, self.max_dimension)
            
            # Extract metadata
            metadata = {
                'width': img.size[0],
                'height': img.size[1],
                'format': img.format,
                'mode': img.mode
            }
            
            return {
                'image': img,
                'metadata': metadata,
                'success': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_body_measurements(self, image_path):
        """
        Extract body measurements from image (placeholder for ML model)
        
        Args:
            image_path: Path to user image
            
        Returns:
            dict: Estimated body measurements
        """
        # In production, this would use pose estimation and body measurement ML models
        # For now, return placeholder values
        return {
            'height_cm': 170,
            'chest_cm': 90,
            'waist_cm': 75,
            'hip_cm': 95,
            'shoulder_width_cm': 42,
            'confidence': 0.75,
            'note': 'Measurements are estimates. For best results, please enter actual measurements.'
        }
    
    def detect_pose(self, image_path):
        """
        Detect body pose in image (placeholder for ML model)
        
        Args:
            image_path: Path to user image
            
        Returns:
            dict: Pose keypoints and data
        """
        # In production, use pose estimation model (e.g., OpenPose, MediaPipe)
        return {
            'keypoints': [],
            'confidence': 0.8,
            'pose_detected': True
        }
    
    def generate_tryon_preview(self, user_image_path, product_image_url):
        """
        Generate virtual try-on preview (placeholder for ML model)
        
        Args:
            user_image_path: Path to user image
            product_image_url: URL of product image
            
        Returns:
            str: Path to generated preview image
        """
        # In production, use virtual try-on ML model (e.g., VITON, CP-VTON)
        # For now, return placeholder
        output_path = f"/tmp/tryon_preview_{os.urandom(8).hex()}.jpg"
        
        # Create a simple placeholder image
        try:
            user_img = Image.open(user_image_path)
            # In production, overlay product on user image
            user_img.save(output_path)
            return output_path
        except Exception as e:
            print(f"Error generating preview: {e}")
            return None
    
    def _resize_image(self, img, max_dimension):
        """
        Resize image while maintaining aspect ratio
        
        Args:
            img: PIL Image object
            max_dimension: Maximum dimension (width or height)
            
        Returns:
            PIL Image: Resized image
        """
        ratio = max_dimension / max(img.size)
        new_size = tuple([int(x * ratio) for x in img.size])
        return img.resize(new_size, Image.Resampling.LANCZOS)
    
    def create_avatar(self, measurements):
        """
        Create avatar based on measurements (placeholder)
        
        Args:
            measurements: User body measurements
            
        Returns:
            dict: Avatar data and image path
        """
        # In production, generate 3D avatar or silhouette
        return {
            'avatar_id': os.urandom(16).hex(),
            'measurements': measurements,
            'image_path': '/static/images/avatar_placeholder.png'
        }
    
    def optimize_for_web(self, image_path, quality=85):
        """
        Optimize image for web display
        
        Args:
            image_path: Path to image
            quality: JPEG quality (1-100)
            
        Returns:
            str: Path to optimized image
        """
        try:
            img = Image.open(image_path)
            
            # Resize for web if too large
            if max(img.size) > self.target_dimension:
                img = self._resize_image(img, self.target_dimension)
            
            # Save optimized version
            output_path = image_path.replace('.jpg', '_optimized.jpg')
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            return output_path
        except Exception as e:
            print(f"Error optimizing image: {e}")
            return image_path
