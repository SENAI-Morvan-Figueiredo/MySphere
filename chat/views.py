from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from .forms import MessageForm
from django.db.models import Q, Max
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ChatForm
from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.FERNET_KEY.encode())

@login_required
@require_POST
def criar_chat_ajax(request):
    form = MessageForm(request.POST, request.FILES)
    if form.is_valid():
        msg = form.save(commit=False)
        msg.remetente = request.user
        msg.chat = Chat
        msg.save()
        return redirect("chat_detail", chat_id=Chat.id)

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

    # Impede acesso indevido
    if request.user not in [chat.user1, chat.user2]:
        return redirect("chat_list")

    chat.messages.exclude(remetente=request.user).filter(lido=False).update(lido=True)
    mensagens = chat.messages.order_by("criado_em")

    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False, remetente=request.user, chat=chat)

            # 🔹 Verifica se há imagem, vídeo ou arquiv

            msg.save()
            return redirect("chat_detail", chat_id=chat.id)
    else:
        form = MessageForm()

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



@login_required
def atualizar_chats(request):
    chats = Chat.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).annotate(
        ultima_msg=Max('messages__criado_em')
    ).order_by("-ultima_msg")

    chat_list = []
    for chat in chats:
        if chat.user1 == request.user:
            user2 = chat.user2
        else:
            user2 = chat.user1

        last_message = chat.messages.last()

        # 🔹 Contar mensagens não lidas
        unread_count = chat.messages.filter(lido=False).exclude(remetente=request.user).count()

        chat_list.append({
            'id': chat.id,
            'username': user2.username,
            'foto_url': user2.foto.url if user2.foto else None,
            'last_message': last_message.conteudo if last_message else '',
            'last_message_time': last_message.criado_em.strftime("%H:%M") if last_message else None,
            'unread_count': unread_count,  # 🔹 adiciona aqui
        })

    return JsonResponse({'chats': chat_list})
