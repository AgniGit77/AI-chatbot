"""
File handling utilities with encryption support
"""
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
from cryptography.fernet import Fernet

class FileHandler:
    """Utility for secure file handling"""
    
    def __init__(self):
        self.upload_folder = os.getenv('UPLOAD_FOLDER', 'uploads')
        self.max_size = int(os.getenv('MAX_UPLOAD_SIZE', 16 * 1024 * 1024))
        
        # Initialize encryption (in production, load from secure storage)
        encryption_key = os.getenv('ENCRYPTION_KEY')
        if encryption_key:
            self.cipher = Fernet(encryption_key.encode())
        else:
            self.cipher = None
        
        # Create upload directories
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure required directories exist"""
        directories = [
            self.upload_folder,
            os.path.join(self.upload_folder, 'user_images'),
            os.path.join(self.upload_folder, 'avatars'),
            os.path.join(self.upload_folder, 'tryon_results')
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def save_user_image(self, file, user_id):
        """
        Save user uploaded image securely
        
        Args:
            file: File object from request
            user_id: User identifier
            
        Returns:
            str: Path to saved file
        """
        # Generate unique filename
        filename = secure_filename(file.filename)
        extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'
        unique_filename = f"{user_id}_{uuid.uuid4().hex[:8]}.{extension}"
        
        # Save path
        user_folder = os.path.join(self.upload_folder, 'user_images', str(user_id))
        os.makedirs(user_folder, exist_ok=True)
        
        file_path = os.path.join(user_folder, unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Encrypt if enabled (optional, for sensitive images)
        # In production, implement actual encryption
        
        return file_path
    
    def save_avatar(self, avatar_data, user_id):
        """
        Save user avatar data
        
        Args:
            avatar_data: Avatar configuration data
            user_id: User identifier
            
        Returns:
            str: Path to saved avatar
        """
        unique_filename = f"{user_id}_avatar_{uuid.uuid4().hex[:8]}.json"
        avatar_folder = os.path.join(self.upload_folder, 'avatars', str(user_id))
        os.makedirs(avatar_folder, exist_ok=True)
        
        file_path = os.path.join(avatar_folder, unique_filename)
        
        # Save avatar data
        with open(file_path, 'w') as f:
            import json
            json.dump(avatar_data, f)
        
        return file_path
    
    def delete_user_files(self, user_id):
        """
        Delete all files for a user
        
        Args:
            user_id: User identifier
        """
        import shutil
        
        directories = [
            os.path.join(self.upload_folder, 'user_images', str(user_id)),
            os.path.join(self.upload_folder, 'avatars', str(user_id)),
            os.path.join(self.upload_folder, 'tryon_results', str(user_id))
        ]
        
        for directory in directories:
            if os.path.exists(directory):
                shutil.rmtree(directory)
    
    def get_file_url(self, file_path):
        """
        Convert file path to URL
        
        Args:
            file_path: Local file path
            
        Returns:
            str: URL to access file
        """
        if file_path.startswith(self.upload_folder):
            relative_path = file_path.replace(self.upload_folder, 'uploads')
            return f"/static/{relative_path}"
        return file_path
    
    def encrypt_file(self, file_path):
        """
        Encrypt a file (placeholder for production implementation)
        
        Args:
            file_path: Path to file to encrypt
        """
        if not self.cipher:
            return
        
        # Read file
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # Encrypt
        encrypted_data = self.cipher.encrypt(data)
        
        # Write back
        with open(file_path, 'wb') as f:
            f.write(encrypted_data)
    
    def decrypt_file(self, file_path):
        """
        Decrypt a file (placeholder for production implementation)
        
        Args:
            file_path: Path to file to decrypt
            
        Returns:
            bytes: Decrypted data
        """
        if not self.cipher:
            with open(file_path, 'rb') as f:
                return f.read()
        
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        
        return self.cipher.decrypt(encrypted_data)
