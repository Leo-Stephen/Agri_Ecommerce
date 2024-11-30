from django.urls import path
from . import views

app_name = 'chatbot_app'

urlpatterns = [
    path('chat/toggle/', views.toggle_chat, name='toggle_chat'),
    path('chat/send/', views.send_message, name='send_message'),
]