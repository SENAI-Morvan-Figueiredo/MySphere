from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from .forms import MessageForm
from django.db.models import Q, Max
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ChatForm

@login_required
@require_POST
def criar_chat_ajax(request):
    form = ChatForm(request.POST, user=request.user, tenant=request.user.tenant)
    if form.is_valid():
        chat = form.save()
        return JsonResponse({
            "success": True,
            "chat": {
                "id": chat.id,
                "user2": chat.user2.username,
                "email": chat.user2.email,
            }
        })
    else:
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

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
        chat_list.append({
            'id': chat.id,
            'username': user2.username,
            'foto_url': user2.foto.url if user2.foto else None,
            'last_message': last_message.conteudo if last_message else '',
            'last_message_time': last_message.criado_em.strftime("%H:%M") if last_message else None,
        })

    return JsonResponse({'chats': chat_list})