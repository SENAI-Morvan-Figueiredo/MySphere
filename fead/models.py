from django.db import models
from tenants.models import Tenant
from accounts.models import User

class Post(models.Model):
    post_id = models.AutoField(primary_key=True, unique=True)
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="posts")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="posts_authored")
    conteudo = models.TextField(null=False, blank=False)
    imagem = models.ImageField(upload_to="posts/", null=True, blank=True)
    criado_em = models.DateField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.id_tenant, self.post_id, self.conteudo

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True, unique=True)
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="comments")
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE,  related_name="comments")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="comments_authored")
    conteudo = models.TextField(null=False, blank=False)
    criado_em = models.DateField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.id_tenant, self.post_id, user_id

class Reaction(models.Model):
    reaction_id = models.AutoField(primary_key=True, unique=True)
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="reactions")
    post_id = models.ForeignKey(Comment, on_delete=models.CASCADE,  related_name="reactions")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="reactions_authored")
    tipo = models.CharField(max_length=50, null=False, blank=False)
    criado_em = models.DateField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.id_tenant, self.post_id, self.user, self.tipo