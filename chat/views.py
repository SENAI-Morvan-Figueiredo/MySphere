from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Message, User
from .forms import MessageForm
from django.db.models import Q, Max
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ChatForm
from cryptography.fernet import Fernet
from django.conf import settings
from django.http import FileResponse, Http404
from django.urls import reverse

fernet = Fernet(settings.FERNET_KEY.encode())

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import Chat, Message, User
from .forms import MessageForm
from django.contrib import messages
import os

@login_required
@require_POST
def criar_chat_ajax(request):
    destinatario_email = request.POST.get("email")
    # ... (validação de e-mail e obtenção de destinatario) ...

    destinatario = get_object_or_404(User, email=destinatario_email)

    # Criar ou obter o chat COM tenant obrigatório
    chat, created = Chat.objects.get_or_create(
        tenant=request.user.tenant,
        user1=request.user,
        user2=destinatario
    )

    # Se quiser criar uma primeira mensagem opcional
    form = MessageForm(request.POST, request.FILES)
    if form.is_valid():
        # 🟢 VERIFICA SE HÁ CONTEÚDO ANTES DE SALVAR!
        conteudo = form.cleaned_data.get("conteudo")
        imagem = form.cleaned_data.get("imagem")
        video = form.cleaned_data.get("video")
        arquivo = form.cleaned_data.get("arquivo")

        if any([conteudo, imagem, video, arquivo]):
            msg = form.save(commit=False)
            msg.remetente = request.user
            msg.chat = chat
            msg.save()
        
    # 🟢 ADICIONAR MENSAGEM DE SUCESSO DO DJANGO (É NECESSÁRIO O IMPORT: from django.contrib import messages)
    from django.contrib import messages # Adicione este import, se não estiver no topo

    if created:
        messages.success(request, f"Chat com {destinatario.username} criado com sucesso!")
    else:
        messages.info(request, f"Chat com {destinatario.username} já existia. Redirecionando.")


    return JsonResponse({
        "status": "ok",
        "chat_id": chat.id,
        "redirect_url": reverse("chat_detail", args=[chat.id])
    })



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
            conteudo = form.cleaned_data.get("conteudo")
            imagem = form.cleaned_data.get("imagem")
            video = form.cleaned_data.get("video")
            arquivo = form.cleaned_data.get("arquivo")

            # ❌ Evita mensagem vazia
            if not any([conteudo, imagem, video, arquivo]):
                return redirect("chat_detail", chat_id=chat.id)

            msg = form.save(commit=False, remetente=request.user, chat=chat)
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
def visualizar_arquivo(request, msg_id, tipo):
    try:
        msg = Message.objects.get(id=msg_id)

        if request.user not in [msg.chat.user1, msg.chat.user2]:
            raise Http404("Acesso negado")

        file_field = getattr(msg, tipo, None)

        if not file_field:
            raise Http404("Arquivo não encontrado")

        # Caminho real do arquivo
        file_path = file_field.path

        # ❗ Se não existe no filesystem → NÃO joga 500
        if not os.path.exists(file_path):
            raise Http404("Arquivo físico não encontrado")

        decrypted_file = msg.get_decrypted_file(file_field)

        if decrypted_file is None:
            raise Http404("Erro ao descriptografar")

        content_type = {
            "imagem": "image/jpeg",
            "video": "video/mp4",
        }.get(tipo, "application/octet-stream")

        return FileResponse(decrypted_file, content_type=content_type)

    except Message.DoesNotExist:
        raise Http404("Mensagem não encontrada")



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

@login_required
@login_required
def atualizar_mensagens(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in [chat.user1, chat.user2]:
        return JsonResponse({'erro': 'acesso negado'}, status=403)

    after = request.GET.get("after")

    if after:
        mensagens = chat.messages.filter(id__gt=after).order_by("criado_em")
    else:
        mensagens = chat.messages.order_by("criado_em")

    def get_view_url(field_name, msg_obj):
        if getattr(msg_obj, field_name):
            return reverse("visualizar_arquivo", args=[msg_obj.id, field_name])
        return None

    msgs_json = []
    for msg in mensagens:
        msgs_json.append({
            "id": msg.id,
            "autor": msg.remetente.username,
            "conteudo": msg.conteudo or "",
            "imagem_url": get_view_url("imagem", msg),
            "video_url": get_view_url("video", msg),
            "arquivo_url": get_view_url("arquivo", msg),
            "hora_utc": msg.criado_em.isoformat(),
            "meu": msg.remetente == request.user,
        })

    return JsonResponse({"mensagens": msgs_json})
