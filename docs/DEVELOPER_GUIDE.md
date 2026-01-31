# AI Fashion Chatbot - Developer Documentation

## Project Overview

The AI Fashion Chatbot is a comprehensive fashion assistance platform that provides virtual try-on capabilities, size recommendations, styling advice, and personalized outfit suggestions.

## Architecture

### Technology Stack

**Backend:**
- Python 3.9+
- Flask 3.0.0 (Web Framework)
- SQLAlchemy 2.0 (ORM)
- OpenCV, Pillow (Image Processing)
- BeautifulSoup4 (Web Scraping)
- Cryptography (Data Encryption)

**Frontend:**
- HTML5
- CSS3 (Custom styling, responsive design)
- Vanilla JavaScript (ES6+)
- Font Awesome Icons

**Database:**
- SQLite (Development)
- PostgreSQL (Production - recommended)

### Project Structure

```
AI-chatbot/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
│
├── backend/
│   ├── models/
│   │   └── database.py        # Database models and ORM
│   ├── routes/
│   │   ├── chat_routes.py     # Chat API endpoints
│   │   ├── tryon_routes.py    # Virtual try-on endpoints
│   │   ├── user_routes.py     # User profile endpoints
│   │   └── privacy_routes.py  # Privacy & data management
│   ├── services/
│   │   ├── chatbot_service.py # Chat logic and intent analysis
│   │   ├── tryon_service.py   # Virtual try-on processing
│   │   ├── style_service.py   # Styling recommendations
│   │   ├── product_service.py # Product data extraction
│   │   ├── user_service.py    # User management
│   │   └── privacy_service.py # Privacy operations
│   └── utils/
│       ├── file_handler.py    # File operations with encryption
│       └── image_processor.py # Image processing utilities
│
├── frontend/
│   ├── templates/
│   │   └── index.html         # Main HTML template
│   └── static/
│       ├── css/
│       │   └── style.css      # Application styles
│       ├── js/
│       │   └── app.js         # Frontend JavaScript
│       └── images/            # Static images
│
├── docs/
│   ├── USER_GUIDE.md          # End-user documentation
│   ├── DEVELOPER_GUIDE.md     # This file
│   └── API_DOCUMENTATION.md   # API reference
│
└── tests/                     # Test suite
    ├── test_chatbot.py
    ├── test_tryon.py
    └── test_api.py
```

## Setup & Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)
- Git

### Installation Steps

1. **Clone the repository:**
```bash
git clone https://github.com/AgniGit77/AI-chatbot.git
cd AI-chatbot
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database:**
```bash
python -c "from backend.models.database import init_db; init_db()"
```

6. **Run the application:**
```bash
python app.py
```

7. **Access the application:**
Open browser to `http://localhost:5000`

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# API Keys (Optional for enhanced features)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Flask Configuration
FLASK_SECRET_KEY=generate_a_secure_random_key
FLASK_ENV=development
FLASK_DEBUG=True

# Database
DATABASE_URL=sqlite:///fashion_chatbot.db

# Security
ENCRYPTION_KEY=generate_encryption_key

# File Storage
UPLOAD_FOLDER=uploads
MAX_UPLOAD_SIZE=16777216

# Privacy
DATA_RETENTION_DAYS=365
ALLOW_ANONYMOUS_MODE=True

# Features
ENABLE_VIRTUAL_TRYON=True
ENABLE_AI_RECOMMENDATIONS=True
ENABLE_SIZE_PREDICTION=True
```

### Generating Secret Keys

```python
# Generate Flask secret key
import secrets
print(secrets.token_hex(32))

# Generate encryption key
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

## Database Models

### User
Stores user profile information.

**Fields:**
- `id`: Primary key
- `username`: Optional username
- `email`: Optional email
- `is_anonymous`: Boolean flag
- `created_at`: Timestamp
- `last_active`: Timestamp
- `preferences`: JSON preferences

### UserMeasurements
Stores encrypted body measurements.

**Fields:**
- `height_cm`, `weight_kg`, `chest_cm`, `waist_cm`, `hip_cm`
- `shoulder_width_cm`, `body_type`, `size_preference`

### ChatHistory
Stores conversation history.

### TryOnHistory
Stores virtual try-on results.

### SavedOutfits
Stores user's saved outfit combinations.

## API Endpoints

### Chat Endpoints

#### POST /api/chat/message
Send a message to the chatbot.

**Request:**
```json
{
  "message": "What size should I get?",
  "context": {}
}
```

**Response:**
```json
{
  "success": true,
  "response": "I can help you find the perfect size!",
  "suggestions": ["Enter measurements", "Upload photo"],
  "action": "request_measurements"
}
```

#### GET /api/chat/history
Get chat history for the current session.

### Virtual Try-On Endpoints

#### POST /api/tryon/upload-image
Upload user image for try-on.

**Form Data:**
- `image`: Image file

**Response:**
```json
{
  "success": true,
  "file_path": "/uploads/user_images/...",
  "message": "Image uploaded successfully"
}
```

#### POST /api/tryon/process
Process virtual try-on request.

**Request:**
```json
{
  "product_url": "https://example.com/product",
  "user_image_path": "/uploads/..."
}
```

**Response:**
```json
{
  "success": true,
  "result_image": "/static/tryon_results/...",
  "fit_analysis": {...},
  "size_recommendation": {...},
  "styling_tips": [...]
}
```

### User Endpoints

#### GET/POST /api/user/measurements
Get or update user measurements.

#### GET/POST /api/user/preferences
Manage style preferences.

#### GET/POST/DELETE /api/user/saved-outfits
Manage saved outfits.

### Privacy Endpoints

#### GET /api/privacy/export-data
Export all user data.

#### POST /api/privacy/delete-data
Delete user data.

```json
{
  "data_type": "all"  // or "images", "measurements", "history"
}
```

## Core Services

### ChatbotService

Handles message processing and intent analysis.

**Key Methods:**
- `process_message()`: Process user message
- `_analyze_intent()`: Determine user intent
- `_generate_response()`: Generate appropriate response

**Intents:**
- virtual_tryon
- size_recommendation
- styling_advice
- product_search
- occasion_styling
- general_query

### TryOnService

Manages virtual try-on functionality.

**Key Methods:**
- `process_tryon()`: Generate virtual try-on
- `analyze_fit()`: Analyze garment fit
- `get_size_recommendation()`: Recommend size

**ML Integration Points:**
- Body measurement extraction
- Pose estimation
- Virtual garment rendering

### StyleService

Provides styling advice and recommendations.

**Key Methods:**
- `get_styling_advice()`: Get styling tips
- `generate_outfit_suggestions()`: Create outfit combinations
- `get_accessory_recommendations()`: Suggest accessories
- `analyze_color_compatibility()`: Check color matching

### ProductService

Fetches and parses product information.

**Key Methods:**
- `get_product_info()`: Extract product data from URL
- `search_similar_products()`: Find alternatives

**Supported Retailers:**
- Generic HTML parsing for most stores
- Extensible for retailer-specific parsers

## Frontend Architecture

### JavaScript Class: FashionChatbot

Main frontend controller.

**Key Methods:**
- `handleSendMessage()`: Send chat messages
- `addMessage()`: Display messages in chat
- `handleImageUpload()`: Upload user photos
- `processTryOn()`: Trigger virtual try-on
- `saveMeasurements()`: Save user measurements

**Accessibility Features:**
- Keyboard shortcuts
- Screen reader announcements
- High contrast mode
- Adjustable font sizes

## Security Considerations

### Data Encryption

- User photos encrypted at rest
- Sensitive measurements encrypted
- HTTPS required in production

### Input Validation

- Sanitize user inputs
- Validate file uploads
- Check file sizes and types

### Session Management

- Secure session cookies
- CSRF protection
- Session timeout

### Privacy Compliance

- GDPR-compliant data handling
- Right to be forgotten
- Data export functionality
- Clear privacy policy

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_chatbot.py

# Run with coverage
pytest --cov=backend tests/
```

### Test Structure

```python
# Example test
def test_chatbot_message():
    service = ChatbotService()
    response = service.process_message(
        message="Hello",
        user_id="test_user",
        session_id="test_session"
    )
    assert response['success'] == True
```

## Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use strong secret keys
- [ ] Configure HTTPS
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up proper logging
- [ ] Configure CORS properly
- [ ] Implement rate limiting
- [ ] Set up monitoring
- [ ] Configure backups

### Deployment Options

**Option 1: Traditional Server**
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Option 2: Docker**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**Option 3: Cloud Platforms**
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run
- Azure App Service

## Future Enhancements

### Planned Features

1. **ML Model Integration**
   - Integrate actual VITON or CP-VTON for try-on
   - Pose estimation with OpenPose
   - Body measurement extraction with computer vision

2. **AI Improvements**
   - GPT-4 integration for better conversations
   - Fine-tuned models for fashion advice
   - Image generation for outfit visualization

3. **Additional Features**
   - Multi-language support
   - Voice commands
   - Social sharing
   - Direct purchase links
   - Wardrobe management

4. **Mobile App**
   - Native iOS app
   - Native Android app
   - Camera integration

### Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Write tests
5. Submit pull request

## Troubleshooting

### Common Development Issues

**Database locked error:**
```python
# Close all database connections properly
from backend.models.database import close_db
close_db(db)
```

**Module import errors:**
```bash
# Ensure __init__.py files exist
touch backend/__init__.py
```

**Port already in use:**
```bash
# Find and kill process
lsof -i :5000
kill -9 <PID>
```

## Performance Optimization

### Caching

Implement caching for:
- Product information
- Style recommendations
- Similar product searches

### Database Optimization

- Add indexes on frequently queried fields
- Use database connection pooling
- Implement query optimization

### Image Optimization

- Resize large images
- Use appropriate compression
- Implement lazy loading

## Monitoring & Logging

### Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Metrics to Track

- Response times
- Error rates
- User engagement
- Try-on success rate
- API usage

## Support

### Getting Help

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check docs folder
- **Email**: dev@fashionchatbot.example.com

### Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [OpenCV Documentation](https://docs.opencv.org/)

---

**Version 1.0** | Last Updated: January 2024
