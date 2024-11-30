from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    """
    Enhanced ChatMessage model with message type and status
    """
    MESSAGE_TYPES = [
        ('general', 'General Query'),
        ('product', 'Product Related'),
        ('order', 'Order Related'),
        ('support', 'Customer Support'),
        ('weather', 'Weather Query'),
        ('market', 'Market Prices'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(help_text="The message sent by the user")
    response = models.TextField(help_text="The response from the chatbot")
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='general')
    is_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Chat with {self.user.username} at {self.created_at}" 