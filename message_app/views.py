from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.db.models import Q
from django.core.paginator import Paginator


from message_app.models import Message

# Create your views here.


@login_required(login_url='login')
def inbox(request):
    user = request.user
    messages = Message.get_messages(user= user)
    active_user = None
    users = None

    if messages:
        message = messages[0]
        active_user = message['user'].username
        users = Message.objects.filter(user = user, recipient = message['user'])
        users.update(is_read=True)

        for  message in messages:
            if message['user'].username == active_user:
                message['unread']=0
        
        context = {
            'users' : users,
            'messages' : messages,
            'active_user' : active_user,
        }
    else:
        context = {}
    
    template = loader.get_template('message_template/message.html')
    return HttpResponse(template.render(context, request))

@login_required
def Users(request, username):
    user = request.user
    messages = Message.get_messages(user=user)
    active_user = username
    users = Message.objects.filter(
        user=user, recipient__username=username)
    users.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0

    context = {
        'users' : users,
        'messages' : messages,
        'active_user' : active_user,
    }

    template = loader.get_template('message_template/message.html')
    return HttpResponse(template.render(context, request))

@login_required
def SendMessage(request):
    from_user = request.user
    to_user = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == 'POST':
        to_user = User.objects.get(username=to_user)
        Message.send_message(from_user, to_user, body)
        return redirect('inbox')
    else:
        HttpResponseBadRequest()


def CheckNewMessage(request):
    New_message_Count = 0
    if request.user.is_authenticated:
        New_message_Count = Message.objects.filter(user=request.user, is_read=False).count()
    
    return{'New_message_Count': New_message_Count}


@login_required
def NewConversation(request, username):
    from_user = request.user
    body = "Says Hello!"

    try:
        to_user = User.objects.get(username = username)
    except Exception as e:
        warning_message = "<h1>Messaging Not Possible</h1>"
        return HttpResponse(warning_message)
    if from_user != to_user:
        Message.send_message(from_user, to_user, body)
    return redirect('inbox')