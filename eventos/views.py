from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evento

@login_required
def listar_eventos(request):
    eventos = Evento.objects.all().order_by('inicio')
    pode_gerenciar = request.user.groups.filter(name="Organizadores").exists() or request.user.is_staff
    return render(request, 'eventos/index.html', {
        'eventos': eventos,
        'pode_gerenciar': pode_gerenciar
    })

from django.contrib import messages
from datetime import datetime

@login_required
def criar_evento(request):
    if not request.user.groups.filter(name="Organizadores").exists() and not request.user.is_staff:
        return redirect('listar_eventos')

    if request.method == 'POST':
        inicio = datetime.fromisoformat(request.POST['inicio'])
        fim = datetime.fromisoformat(request.POST['fim'])

        # 🚫 validação: o fim não pode ser antes do início
        if fim < inicio:
            messages.error(request, "A data de término não pode ser anterior à data de início.")
            return render(request, 'eventos/formulario.html', {'acao': 'criar'})

        Evento.objects.create(
            titulo=request.POST['titulo'],
            descricao=request.POST.get('descricao', ''),
            inicio=inicio,
            fim=fim,
            criado_por=request.user,
            tenant=request.user.tenant
        )
        messages.success(request, "Evento criado com sucesso!")
        return redirect('listar_eventos')
    

    return render(request, 'eventos/formulario.html', {'acao': 'criar'})


@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if evento.criado_por != request.user and not request.user.is_staff:
        return redirect('listar_eventos')

    if request.method == 'POST':
        evento.titulo = request.POST['titulo']
        evento.descricao = request.POST.get('descricao', '')
        evento.inicio = request.POST['inicio']
        evento.fim = request.POST['fim']
        evento.save()
        return redirect('listar_eventos')
    return render(request, 'eventos/formulario.html', {'evento': evento, 'acao': 'editar'})

@login_required
def excluir_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if evento.criado_por == request.user or request.user.is_staff:
        evento.delete()
    return redirect('listar_eventos')
