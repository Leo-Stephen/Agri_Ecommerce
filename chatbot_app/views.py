from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.http import HttpResponse, JsonResponse
from .models import ChatMessage
from .ai_service import GeminiService
from django.urls import reverse
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)
gemini_service = GeminiService()

@require_http_methods(["POST"])
def send_message(request):
    if not request.user.is_authenticated:
        return HttpResponse(
            '<div class="message bot-message">'
            f'<p>Please <a href="{reverse("login")}?next={request.path}">log in</a> to start chatting</p>'
            '</div>',
            status=401
        )
    
    message = request.POST.get('message', '').strip()
    if not message:
        return JsonResponse({'status': 'error', 'message': 'Message cannot be empty'}, status=400)
        
    try:
        message_type = determine_message_type(message)
        user_type = 'farmer' if hasattr(request.user, 'farmerprofile') else 'customer'
        
        ai_response = gemini_service.get_response(message, user_type, message_type)
        if ai_response is None:
            ai_response = get_bot_response(message, user_type, message_type)
        
        ChatMessage.objects.create(user=request.user, message=message, message_type=message_type, is_user=True)
        ChatMessage.objects.create(user=request.user, message=ai_response['text'], message_type=message_type, is_user=False)
        
        return TemplateResponse(request, 'chatbot_app/messages.html', {
            'messages': ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:2]
        })
        
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def determine_message_type(message):
    message = message.lower()
    if any(word in message for word in ['price', 'cost', 'rate', 'market']): return 'market'
    elif any(word in message for word in ['weather', 'rain', 'temperature']): return 'weather'
    elif any(word in message for word in ['order', 'delivery', 'track']): return 'order'
    elif any(word in message for word in ['product', 'stock', 'available']): return 'product'
    elif any(word in message for word in ['help', 'support', 'contact']): return 'support'
    return 'general'

def get_bot_response(message, user_type, message_type):
    if user_type == 'farmer':
        return get_farmer_response(message, message_type)
    return get_customer_response(message, message_type)

@require_http_methods(["GET"])
def toggle_chat(request):
    logger.debug(f'Toggle chat called - Method: {request.method}')
    logger.debug(f'User: {request.user}')
    
    if not request.user.is_authenticated:
        logger.debug('User not authenticated')
        return HttpResponse(status=401)
    
    is_visible = request.session.get('chat_visible', False)
    request.session['chat_visible'] = not is_visible
    logger.debug(f'Chat visibility toggled to: {not is_visible}')
    
    if not is_visible:  # Opening the chat
        messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:10]
        logger.debug(f'Found {len(messages)} messages')
        
        # Add an initial bot message if no messages exist
        if not messages:
            initial_message = "Hello! How can I assist you today?"
            ChatMessage.objects.create(
                user=request.user,
                message=initial_message,
                is_user=False,
                message_type='general'
            )
            messages = [ChatMessage.objects.filter(user=request.user).latest('created_at')]
        
        return TemplateResponse(request, 'chatbot_app/chat_widget.html', {
            'messages': messages,
            'show_chat_content': True
        })
    
    logger.debug('Returning empty response for chat close')
    return HttpResponse('')