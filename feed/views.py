from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Max
from .models import Post, Comment, Like, Share, Hashtag
from accounts.models import User
from chat.models import Chat
from django.template.loader import render_to_string
from django.http import HttpResponse
from eventos.models import Evento
from django.utils import timezone
import time
from django.conf import settings
from django.template.loader import render_to_string

# Define o tempo máximo de espera (em segundos)
LONG_POLLING_TIMEOUT = 10 # 10 segundos de espera
CHECK_INTERVAL = 1 # Verificar a cada 1 segundo

@login_required
def feed_view(request):
    posts = Post.objects.filter(
        tenant=request.user.tenant
    ).select_related('user').prefetch_related('likes', 'comments', 'shares', 'hashtags')

    for post in posts:
        post.user_has_liked = post.likes.filter(user=request.user).exists()

    chats = Chat.objects.filter(
        Q(user1=request.user) | Q(user2=request.user),
        messages__isnull=False
    ).annotate(
        ultima_msg=Max('messages__criado_em')
    ).order_by('-ultima_msg')[:5]

    # 🔹 Aqui busca os eventos do mesmo tenant do usuário
    eventos = Evento.objects.filter(
        tenant=request.user.tenant
    ).order_by('inicio')

    # 🔹 Se quiser, restringe aos próximos eventos:
    hoje = timezone.now()
    eventos = (
        Evento.objects.filter(fim__gte=hoje)  # só os que ainda vão acontecer
        .order_by('fim')                      # ordena do mais próximo pro mais distante
    )[:3]  # limita aos 5 primeiros
    

    pode_gerenciar = request.user.is_staff or request.user.groups.filter(name='Organizadores').exists()
    latest_post = Post.objects.filter(tenant=request.user.tenant).first()
    latest_post_id = latest_post.post_id if latest_post else 0

    context = {
        'posts': posts,
        'chats': chats,
        'eventos': eventos,
        'pode_gerenciar': pode_gerenciar,
        'user': request.user,
        'latest_post_id': latest_post_id, # 👈 Adicionado o ID do post mais recente
    }
    return render(request, 'feed/feed.html', context)


@login_required
def atualizar_chats(request):
    chats = Chat.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).annotate(
        ultima_msg=Max('messages__criado_em')
    ).order_by('-ultima_msg')[:5]

    html = render_to_string('feed/atualizar_chats.html', {'chats': chats, 'request': request})
    return HttpResponse(html)

@login_required
@require_POST
def create_post(request):
    conteudo = request.POST.get('conteudo', '').strip()
    arquivo_media = request.FILES.get('imagem')
    arquivo_file = request.FILES.get('arquivo')
    
    imagem = None
    video = None
    arquivo = arquivo_file
    
    if arquivo_media:
        content_type = arquivo_media.content_type
        if content_type.startswith('video/'):
            video = arquivo_media
        elif content_type.startswith('image/'):
            imagem = arquivo_media
    
    if conteudo or imagem or video or arquivo:
        post = Post.objects.create(
            tenant=request.user.tenant,
            user=request.user,
            conteudo=conteudo,
            imagem=imagem,
            video=video,
            arquivo=arquivo
        )
        
        # Extrair e criar hashtags
        hashtags = post.extract_hashtags()
        for tag in hashtags:
            hashtag_obj, created = Hashtag.objects.get_or_create(
                tenant=request.user.tenant,
                tag=tag.lower()
            )
            post.hashtags.add(hashtag_obj)
        
        # Extrair e associar menções
        mencoes = post.extract_mentions()
        for username in mencoes:
            try:
                user_mencionado = User.objects.get(username=username, tenant=request.user.tenant)
                post.mencoes.add(user_mencionado)
            except User.DoesNotExist:
                pass
    
    return redirect('feed:feed')

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id, tenant=request.user.tenant)
    
    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user,
        tenant=request.user.tenant
    )
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes()
    })

@login_required
@require_POST
def comment_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id, tenant=request.user.tenant)
    conteudo = request.POST.get('conteudo', '').strip()
    
    if conteudo:
        comment = Comment.objects.create(
            tenant=request.user.tenant,
            post=post,
            user=request.user,
            conteudo=conteudo
        )
        
        return JsonResponse({
            'success': True,
            'comment': {
                'user': comment.user.username,
                'conteudo': comment.conteudo,
                'criado_em': comment.criado_em.strftime('%d/%m/%Y %H:%M')
            },
            'total_comments': post.total_comments()
        })
    
    return JsonResponse({'success': False}, status=400)

@login_required
@require_POST
def share_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id, tenant=request.user.tenant)
    
    Share.objects.create(
        post=post,
        user=request.user,
        tenant=request.user.tenant
    )
    
    return JsonResponse({
        'success': True,
        'total_shares': post.total_shares()
    })

@login_required
def hashtag_view(request, tag):
    """View para mostrar posts com uma hashtag específica"""
    hashtag = get_object_or_404(Hashtag, tag=tag.lower(), tenant=request.user.tenant)
    posts = hashtag.posts.filter(tenant=request.user.tenant).select_related('user').prefetch_related('likes', 'comments', 'shares', 'hashtags')
    
    for post in posts:
        post.user_has_liked = post.likes.filter(user=request.user).exists()
    
    context = {
        'posts': posts,
        'user': request.user,
        'hashtag': hashtag,
    }
    return render(request, 'feed/hashtag.html', context)

@login_required
def search_view(request):
    """View para pesquisar usuários e hashtags de forma inteligente"""
    query = request.GET.get('q', '').strip()
    tenant_id = request.user.tenant
    
    results = {
        'users': [],
        'hashtags': [],
        'posts': [],
        'query': query
    }
    
    if query:
        # Busca inteligente baseada no tipo de query
        if query.startswith('#'):
            # Busca específica por hashtag
            tag = query[1:]
            results['hashtags'] = Hashtag.objects.filter(
                tag__icontains=tag,
                tenant=tenant_id
            ).prefetch_related('posts')[:10]
            
            # Buscar posts com a hashtag
            results['posts'] = Post.objects.filter(
                tenant=tenant_id,
                conteudo__icontains=query
            ).select_related('user').prefetch_related('likes', 'comments')[:20]
            
        elif query.startswith('@'):
            # Busca específica por usuário
            username = query[1:]
            results['users'] = User.objects.filter(
                Q(username__icontains=username) | Q(first_name__icontains=username) | Q(last_name__icontains=username),
                tenant=tenant_id
            )[:10]
            
        else:
            # Busca mista: usuários e hashtags
            results['users'] = User.objects.filter(
                Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query),
                tenant=tenant_id
            )[:10]
            
            results['hashtags'] = Hashtag.objects.filter(
                tag__icontains=query,
                tenant=tenant_id
            ).prefetch_related('posts')[:10]
    
    context = {
        'results': results,
        'user': request.user,
    }
    return render(request, 'feed/search.html', context)

@login_required
def autocomplete_view(request):
    """API endpoint para autocompletar @ e #"""
    query_type = request.GET.get('type', '')
    query = request.GET.get('q', '').strip()
    tenant_id = request.user.tenant
    results = []
    
    if query:
        if query_type == 'user':
            # Autocompletar usuários
            users = User.objects.filter(
                Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query),
                tenant=tenant_id
            )[:5]
            
            results = [{
                'username': user.username,
                'name': user.get_full_name() or user.username
            } for user in users]
            
        elif query_type == 'hashtag':
            # Autocompletar hashtags
            hashtags = Hashtag.objects.filter(
                tag__icontains=query,
                tenant=tenant_id
            )[:5]
            
            results = [{
                'tag': hashtag.tag,
                'count': hashtag.posts.count()
            } for hashtag in hashtags]
    
    return JsonResponse(results, safe=False)

@login_required
def check_new_posts(request):
    print("📡 Check_new_posts foi chamado!")
    last_post_id = request.GET.get('last_post_id', 0)
    try:
        last_post_id = int(last_post_id)
    except ValueError:
        last_post_id = 0

    start_time = time.time()

    while time.time() - start_time < LONG_POLLING_TIMEOUT:
        new_posts = Post.objects.filter(
            tenant=request.user.tenant,
            post_id__gt=last_post_id
        ).select_related('user').prefetch_related('likes', 'comments', 'shares', 'hashtags').order_by('-criado_em')

        if new_posts.exists():
            latest_post_id = new_posts.first().post_id

            # Transformar posts em JSON
            posts_json = []
            for p in new_posts:
                posts_json.append({
                    "id": p.post_id,
                    "conteudo": p.conteudo_formatado,
                    "user": {
                        "id": p.user.id,
                        "username": p.user.username,
                        "nome": p.user.get_full_name() or p.user.username,
                        "foto": p.user.foto.url if p.user.foto else None
                    },
                    "criado_em": p.criado_em.strftime('%d %b at %H:%M'),
                    "imagem": p.imagem.url if p.imagem else None,
                    "video": p.video.url if p.video else None,
                    "arquivo": p.arquivo.url if p.arquivo else None,
                    "arquivo_nome": p.arquivo.name[6:] if p.arquivo else None,
                    "likes": p.total_likes(),
                    "comments": p.total_comments(),
                    "shares": p.total_shares(),
                    "user_has_liked": p.likes.filter(user=request.user).exists(),
                })

            return JsonResponse({
                'status': 'updated',
                'latest_post_id': latest_post_id,
                'posts': posts_json
            })

        time.sleep(CHECK_INTERVAL)

    return JsonResponse({
        'status': 'timeout',
        'latest_post_id': last_post_id
    })