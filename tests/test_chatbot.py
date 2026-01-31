"""
Test suite for AI Fashion Chatbot
"""
import pytest
from backend.services.chatbot_service import ChatbotService
from backend.services.style_service import StyleService
from backend.services.product_service import ProductService

def test_chatbot_service_initialization():
    """Test chatbot service can be initialized"""
    service = ChatbotService()
    assert service is not None
    assert service.max_context == 10

def test_intent_analysis():
    """Test intent analysis functionality"""
    service = ChatbotService()
    
    # Test virtual try-on intent
    intent = service._analyze_intent("I want to try on clothes")
    assert intent == 'virtual_tryon'
    
    # Test size recommendation intent
    intent = service._analyze_intent("What size should I get?")
    assert intent == 'size_recommendation'
    
    # Test styling advice intent
    intent = service._analyze_intent("How should I style this?")
    assert intent == 'styling_advice'

def test_style_service():
    """Test style service"""
    service = StyleService()
    
    # Test outfit generation
    outfits = service.generate_outfit_suggestions(
        base_item="shirt",
        occasion="casual",
        user_id="test_user"
    )
    assert len(outfits) > 0
    assert 'name' in outfits[0]
    assert 'items' in outfits[0]

def test_product_service():
    """Test product service"""
    service = ProductService()
    
    # Test with mock URL
    product_info = service._get_mock_product_data("https://example.com/product")
    assert product_info['name'] is not None
    assert product_info['price'] is not None
    assert 'sizes' in product_info

def test_response_generation():
    """Test response generation"""
    service = ChatbotService()
    
    response = service._generate_response(
        intent='general_query',
        message='Hello',
        user_id='test_user',
        context={}
    )
    
    assert 'message' in response
    assert 'suggestions' in response
    assert len(response['suggestions']) > 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
