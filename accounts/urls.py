from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import Users, UserLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', views.feed_view, name='home'),
    path("atualizar_sobre/", views.atualizar_sobre, name="atualizar_sobre"),
    path("perfil/<int:pk>/", views.feed_perfil_view, name='perfil'),
    path('perfil/<int:post_id>/like/<int:pk>/', views.like_post_perfil, name='like_post'),
    path('perfil/<int:post_id>/comment/<int:pk>/', views.comment_post_perfil, name='comment_post'),
    path('perfil/<int:post_id>/share/<int:pk>/', views.share_post_perfil, name='share_post'),
    path('home/<int:post_id>/like/', views.like_post_home, name='like_post'),
    path('home/<int:post_id>/comment/', views.comment_post_home, name='comment_post'),
    path('home/<int:post_id>/share/', views.share_post_home, name='share_post'),
    
    # TROCAR SENHA
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    
    # URLS DE RESET DE SENHA
    path('password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt'
        ),
        name='password_reset'
    ),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html' ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]