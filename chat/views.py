from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from .forms import MessageForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Chat, Message
from .forms import MessageForm
from django.contrib.auth.decorators import login_required

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    mensagens = chat.messages.order_by('criado_em')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.chat = chat
            msg.remetente = request.user
            msg.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()
    
    return render(request, 'chat/chat_detail.html', {'chat': chat, 'mensagens': mensagens, 'form': form})

@login_required
def chat_list(request):
    chats = Chat.objects.filter(user1=request.user) | Chat.objects.filter(user2=request.user)
    return render(request, "chat/chat_list.html", {"chats": chats})

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in [chat.user1, chat.user2]:
        return redirect("chat_list")

    messages = chat.messages.order_by("criado_em")
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.chat = chat
            msg.remetente = request.user
            msg.save()
            return redirect("chat_detail", chat_id=chat.id)
    else:
        form = MessageForm()

    return render(request, "chat/chat_detail.html", {"chat": chat, "messages": messages, "form": form})
