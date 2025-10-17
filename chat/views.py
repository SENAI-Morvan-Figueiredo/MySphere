from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from .forms import MessageForm
from django.db.models import Q, Max

@login_required
def chat_list(request):
    # 🔹 Buscar todos os chats do usuário, sem duplicar
    chats = Chat.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).annotate(
        ultima_msg=Max('messages__criado_em')
    ).order_by('-ultima_msg')

    return render(request, "chat/chat_list.html", {"chats": chats})


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    # Segurança — impede abrir chat que não pertence ao usuário
    if request.user not in [chat.user1, chat.user2]:
        return redirect("chat_list")

    mensagens = chat.messages.order_by("criado_em")

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

    # 🔹 Buscar todos os chats sem duplicar (igual acima)
    chats = Chat.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).annotate(
        ultima_msg=Max('messages__criado_em')
    ).order_by('-ultima_msg')

    context = {
        "chat": chat,
        "mensagens": mensagens,
        "form": form,
        "chats": chats,
    }
    return render(request, "chat/chat_detail.html", context)
