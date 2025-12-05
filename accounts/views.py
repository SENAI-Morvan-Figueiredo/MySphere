from feed.models import Post, Comment, Like, Share
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from .models import User
from django.urls import reverse_lazy, reverse
from django.views import View
from feed.models import Post
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.views.decorators.http import require_POST
from .forms import UserEditFormStaff
from django.contrib.auth import views as auth_views
from chat.models import Chat

# Create your views here.




@login_required
def open_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id, tenant=request.user.tenant)

    # Impedir chat com si mesmo
    if other_user == request.user:
        return redirect('chat_list')

    # Procurar chat existente (ordem não importa)
    chat = Chat.objects.filter(
        tenant=request.user.tenant,
        user1__in=[request.user, other_user],
        user2__in=[request.user, other_user]
    ).first()

    # Criar se não existir
    if not chat:
        chat = Chat.objects.create(
            tenant=request.user.tenant,
            user1=request.user,
            user2=other_user
        )

    return redirect('chat_detail', chat_id=chat.id)




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

        total_likes = Like.objects.filter(post__user=profile_user).count()
        total_comments = Comment.objects.filter(post__user=profile_user).count()

        context = {
            'posts': posts,
            'profile_user': profile_user,
            'user': request.user,
            'total_likes': total_likes,
            'total_comments': total_comments,
        }


    return render(request, 'accounts/account_home.html', context)




@login_required
def feed_perfil_view(request, pk):

    profile_user = get_object_or_404(User, id=pk)

    posts = (
        Post.objects.filter(
            tenant=profile_user.tenant,
            user=profile_user
        )
        .select_related('user')
        .prefetch_related('likes', 'comments', 'shares', 'hashtags')
        .order_by('-criado_em')
    )

    # Likes recebidos
    total_likes = Like.objects.filter(post__user=profile_user).count()

    # Comentários recebidos
    total_comments = Comment.objects.filter(post__user=profile_user).count()

    # Marca se o usuário atual curtiu cada post
    for post in posts:
        post.user_has_liked = post.likes.filter(user=request.user).exists()

    context = {
        'posts': posts,
        'profile_user': profile_user,

        # novos campos
        'total_likes': total_likes,
        'total_comments': total_comments,
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

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'  
        
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse('tenant_list')
        return reverse('feed:feed')
    
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

# VIEW QUE DELETA E EDIT USER PELO STAFF

class UserStaffDeleteView(DeleteView):
    model = User
    template_name = 'staff/staff_users.html'
    success_url = reverse_lazy('users_staff')
    
class UserStaffEditView(UpdateView):
    model = User
    form_class = UserEditFormStaff
    template_name = 'staff/staff_users_form.html'
    success_url = reverse_lazy('users_staff')
 
# VIEW QUE ENVIA O EMAIL

class ResetPasswordView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    html_email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')