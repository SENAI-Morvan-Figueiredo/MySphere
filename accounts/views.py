from feed.models import Post, Comment, Like, Share
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from .models import User
from .forms import UserForm
from django.urls import reverse_lazy
from django.views import View
from feed.models import Post
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.views.decorators.http import require_POST

# Create your views here.


@login_required
def feed_view(request, username=None):
    # Se for perfil de outro usuário
    if username:
        profile_user = get_object_or_404(User, username=username, tenant=request.user.tenant)
    else:
        # Se for o próprio perfil
        profile_user = request.user

    # Filtra os posts do usuário específico dentro do mesmo tenant
    posts = (
        Post.objects.filter(
            tenant=profile_user.tenant,
            user=profile_user
        )
        .select_related('user')
        .prefetch_related('likes', 'comments', 'shares', 'hashtags')
        .order_by('-criado_em')
    )

    # Marca se o usuário atual curtiu cada post
    for post in posts:
        post.user_has_liked = post.likes.filter(user=request.user).exists()

    context = {
        'posts': posts,
        'profile_user': profile_user,  # <-- agora o template sabe de quem é o perfil
        'user': request.user,
    }

    return render(request, 'accounts/account_home.html', context)




@login_required
def feed_perfil_view(request, pk):
    # Se for perfil de outro usuário
    
    profile_user = get_object_or_404(User, id=pk)

    # Filtra os posts do usuário específico dentro do mesmo tenant
    posts = (
        Post.objects.filter(
            tenant=profile_user.tenant,
            user=profile_user
        )
        .select_related('user')
        .prefetch_related('likes', 'comments', 'shares', 'hashtags')
        .order_by('-criado_em')
    )

    # Marca se o usuário atual curtiu cada post
    for post in posts:
        post.user_has_liked = post.likes.filter(user=request.user).exists()

    context = {
        'posts': posts,
        'profile_user': profile_user,  # <-- agora o template sabe de quem é o perfil
    }

    return render(request, 'accounts/account_perfil.html', context)




@login_required
@csrf_exempt
def atualizar_sobre(request):
    if request.method == "POST":
        data = json.loads(request.body)
        novo_sobre = data.get("sobre_mim", "").strip()

        user = request.user
        user.sobre_mim = novo_sobre
        user.save()

        return JsonResponse({"success": True, "novo_sobre": user.sobre_mim})

    return JsonResponse({"success": False}, status=400)



class Users(ListView):
    model = User
    template_name = "accounts/account_list.html"
    context_object_name = "users"
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(tenant=self.request.user.tenant)
        return User.objects.none()

# class Home(ListView):
#     model = User
#     template_name = "accounts/account_home.html"
#     context_object_name = "users"

class novo(CreateView):
    model = User
    form_class = UserForm
    template_name = "accounts/add.html"
    success_url = reverse_lazy('users')

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'  
    redirect_authenticated_user = True     
    
    
ROOT_URLCONF = 'MySphere.urls'



@login_required
@require_POST
def like_post_home(request, post_id):
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
def comment_post_home(request, post_id):
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
#
@login_required
@require_POST
def share_post_home(request, post_id):
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



#_________________________________________________________________________________________________________________



@login_required
@require_POST
def like_post_perfil(request, post_id):
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
def comment_post_perfil(request, post_id):
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
def share_post_perfil(request, post_id):
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
#_________________________________________________________________________________________________________________

