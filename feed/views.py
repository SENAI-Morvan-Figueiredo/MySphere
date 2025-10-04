from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Post, Comment, Like, Share, Hashtag
from accounts.models import User

@login_required
def feed_view(request):
    posts = Post.objects.filter(tenant=request.user.tenant).select_related('user').prefetch_related('likes', 'comments', 'shares', 'hashtags')
    
    for post in posts:
        post.user_has_liked = post.likes.filter(user=request.user).exists()
    
    context = {
        'posts': posts,
        'user': request.user,
    }
    return render(request, 'feed/feed.html', context)

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
