from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evento
from django.contrib import messages
from datetime import datetime

@login_required
def listar_eventos(request, modo=None):
    eventos = Evento.objects.all().order_by('inicio')
    pode_gerenciar = request.user.is_staff

    template = 'eventos/list_eventos.html' if modo == 'compacto' else 'eventos/index.html'

    return render(request, template, {
        'eventos': eventos,
        'pode_gerenciar': pode_gerenciar
    })




@login_required
def criar_evento(request):
    if request.method == 'POST':

        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        inicio_str = request.POST.get('inicio')
        fim_str = request.POST.get('fim')
        foto = request.FILES.get('foto')  

        try:
            inicio = datetime.fromisoformat(inicio_str)
            fim = datetime.fromisoformat(fim_str)
        except ValueError:
            messages.get_messages(request).used = True
            messages.error(request, "Datas inválidas. Verifique o formato e tente novamente.")
            return render(request, 'eventos/formulario.html', {'acao': 'criar'})

        # 🚫 validação: o fim não pode ser antes do início
        if fim < inicio:
            messages.get_messages(request).used = True
            messages.error(request, "A data de término não pode ser anterior à data de início.")
            return render(request, 'eventos/formulario.html', {'acao': 'criar'})

        # ✅ tudo certo — salvar evento
        evento = Evento.objects.create(
            titulo=titulo,
            descricao=descricao,
            inicio=inicio,
            fim=fim,
            foto=foto,
            criado_por=request.user,
            tenant=request.user.tenant  # assume que vem do usuário
        )

        messages.get_messages(request).used = True
        messages.success(
            request,
            f"Evento '{evento.titulo}' criado com sucesso por {request.user.username} em {datetime.now().strftime('%d/%m/%Y %H:%M')}."
        )
        return redirect('listar_eventos')
    
    
    return render(request, 'eventos/formulario.html', {'acao': 'criar'})


@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    # só o criador ou staff podem editar
    if evento.criado_por != request.user and not request.user.is_staff:
        return redirect('listar_eventos')

    if request.method == 'POST':
        try:
            inicio = datetime.fromisoformat(request.POST['inicio'])
            fim = datetime.fromisoformat(request.POST['fim'])
        except ValueError:
            messages.error(request, "Datas inválidas. Verifique o formato e tente novamente.")
            return render(request, 'eventos/formulario.html', {'evento': evento, 'acao': 'editar'})

        # 🚫 validação: fim não pode ser antes do início
        if fim < inicio:
            messages.get_messages(request).used = True  # limpa mensagens antigas
            messages.error(request, "A data de término não pode ser anterior à data de início.")
            return render(request, 'eventos/formulario.html', {'evento': evento, 'acao': 'editar'})

        # ✅ se passou na validação, atualiza normalmente
        evento.titulo = request.POST['titulo']
        evento.descricao = request.POST.get('descricao', '')
        evento.inicio = inicio
        evento.fim = fim
        evento.save()

        messages.get_messages(request).used = True
        messages.success(request, f"Evento atualizado com sucesso por {request.user.username} em {datetime.now().strftime('%d/%m/%Y %H:%M')}.")
        return redirect('listar_eventos')
    
    # GET → mostra o formulário preenchido
    return render(request, 'eventos/formulario.html', {'evento': evento, 'acao': 'editar'})


@login_required
def excluir_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if evento.criado_por == request.user or request.user.is_staff:
        nome_evento = evento.titulo  # só pra exibir o nome na mensagem
        evento.delete()
        messages.success(request, f'O evento "{nome_evento}" foi excluído com sucesso!')
    else:
        messages.error(request, "Você não tem permissão para excluir este evento.")
    return redirect('listar_eventos')