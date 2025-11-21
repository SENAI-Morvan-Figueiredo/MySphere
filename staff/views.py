from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from accounts.models import User
from feed.models import Post, Comment, Hashtag, Share, Like
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from tenants.models import Tenant
from .forms import FormAddUsersStaff
from django.urls import reverse_lazy
from .mixins import StaffRequiredMixin

def error_403_view(request, exception=None):
    return render(request, 'staff/403.html', status=403)

class DashboardPageView(TemplateView):
    template_name = "staff/staff_home.html"

    def get_context_data(self, **kwargs):
        tenant = self.request.user.tenant

        context = super().get_context_data(**kwargs)

        context["total_users"] = User.objects.filter(tenant=tenant).count()
        context["total_posts"] = Post.objects.filter(tenant=tenant).count()
        context["total_comments"] = Comment.objects.filter(tenant=tenant).count()
        context["total_hashtags"] = Hashtag.objects.filter(tenant=tenant).count()

        hoje = timezone.now().date()
        dias = [hoje - timedelta(days=i) for i in range(6, -1, -1)]

        labels = [dia.strftime("%d/%m") for dia in dias]
        counts = [
            Post.objects.filter(
                tenant=tenant,
                criado_em__date=dia
            ).count()
            for dia in dias
        ]

        context["posts_labels"] = labels
        context["posts_counts"] = counts

        total_likes = Like.objects.filter(tenant=tenant).count()
        total_comments = Comment.objects.filter(tenant=tenant).count()
        total_shares = Share.objects.filter(tenant=tenant).count()

        context["engajamento"] = [total_likes, total_comments, total_shares]

        hashtags_qs = (
            Hashtag.objects.filter(tenant=tenant)
            .annotate(qtd=Count("posts"))
            .order_by("-qtd")[:5]
        )
        context["hashtags_labels"] = [h.tag for h in hashtags_qs]
        context["hashtags_counts"] = [h.qtd for h in hashtags_qs]

        context["recent_posts"] = Post.objects.filter(tenant=tenant).order_by("-criado_em")[:5]

        return context

class AddUsersStaffView(CreateView):
    model = User
    form_class = FormAddUsersStaff
    template_name = "staff/users.html"
    success_url = reverse_lazy('users_staff')

    def form_valid(self, form):
        tenant_id = self.request.user.tenant.pk
        self.object = form.save(commit=False) 
        self.object.tenant_id = tenant_id
        self.object.save()
        return super().form_valid(form) 

class UsersPageView(StaffRequiredMixin, TemplateView):
    template_name = "staff/staff_users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FormAddUsersStaff()
        context["users"] = User.objects.filter(tenant=self.request.user.tenant)
        return context

    def post(self, request, *args, **kwargs):
            form = FormAddUsersStaff(request.POST, request.FILES)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.tenant = request.user.tenant
                new_user.save()
                return redirect("users_staff") 
            
            context = self.get_context_data()
            context["form"] = form
            
            return self.render_to_response(context)