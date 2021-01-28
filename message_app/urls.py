from message_app.views import inbox, Users, SendMessage, NewConversation
from django.urls import path
# from . import views

urlpatterns = [
    path('', inbox, name="inbox"),
    path('users/<username>', Users, name='users'),
    path('send/', SendMessage, name='send_message'),
    path('new/<username>', NewConversation, name='new_conversation'),
]
