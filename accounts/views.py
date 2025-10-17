from django.shortcuts import render, redirect
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

from django.http import JsonResponse

@login_required
@csrf_exempt
def atualizar_sobre(request):
    if request.method == "POST":
        data = json.loads(request.body)
        novo_sobre = data.get("sobre_mim", "").strip()
        user = request.user
        user.sobre_mim = novo_sobre
        user.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "erro", "mensagem": "Método inválido"}, status=400)

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
