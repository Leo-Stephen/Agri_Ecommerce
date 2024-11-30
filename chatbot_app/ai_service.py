import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ChatbotError(Exception):
    """Base exception for chatbot-related errors"""
    pass

class GeminiServiceError(ChatbotError):
    """Raised when there's an error with Gemini service"""
    pass

class GeminiService:
    def __init__(self):
        try:
            if not settings.GEMINI_API_KEY:
                raise GeminiServiceError("Gemini API key not found")
            
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            self._test_connection()
            
        except Exception as e:
            logger.error(f"Gemini initialization error: {str(e)}")
            raise GeminiServiceError(f"Failed to initialize Gemini: {str(e)}")
    
    def _test_connection(self):
        try:
            test_response = self.model.generate_content("Test connection")
            if not test_response:
                raise GeminiServiceError("No response from Gemini API")
        except Exception as e:
            raise GeminiServiceError(f"Connection test failed: {str(e)}")
    
    def get_response(self, message, user_type, message_type):
        try:
            prompt = f"""As Kisan Vishwa's AI assistant for {user_type}s:
            - Message type: {message_type}
            - User query: {message}
            
            For farmers, help with:
            - Market prices and trends
            - Weather and crop advice
            - Inventory management
            
            For customers, help with:
            - Product information
            - Order tracking
            - Shopping assistance
            
            Provide a helpful, concise response."""
            
            response = self.model.generate_content(prompt)
            return {
                'text': response.text,
                'message_type': message_type
            }
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return None