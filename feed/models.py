from django.db import models
from tenants.models import Tenant
from accounts.models import User
import re

class Hashtag(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="hashtags")
    tag = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('tenant', 'tag')
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"#{self.tag}"

class Post(models.Model):
    post_id = models.AutoField(primary_key=True, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="posts")
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="posts_authored")
    conteudo = models.TextField(null=False, blank=False)
    imagem = models.ImageField(upload_to="posts/", null=True, blank=True)
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    arquivo = models.FileField(upload_to="files/", null=True, blank=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="posts", blank=True)
    mencoes = models.ManyToManyField(User, related_name="mentioned_in", blank=True)
    criado_em = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f"Post by {self.user.username} at {self.criado_em}"
    
    def total_likes(self):
        return self.likes.count()
    
    def total_comments(self):
        return self.comments.count()
    
    def total_shares(self):
        return self.shares.count()
    
    def extract_hashtags(self):
        """Extrai hashtags do conteúdo do post"""
        return re.findall(r'#(\w+)', self.conteudo)
    
    def extract_mentions(self):
        """Extrai menções (@username) do conteúdo do post"""
        return re.findall(r'@(\w+)', self.conteudo)
    
    def conteudo_formatado(self):
        """Retorna o conteúdo com hashtags e menções formatadas como links"""
        texto = self.conteudo
        
        # Formatar hashtags
        hashtags = re.findall(r'#(\w+)', texto)
        for tag in hashtags:
            texto = texto.replace(f'#{tag}', f'<a href="/hashtag/{tag}/" class="hashtag">#{tag}</a>')
        
        # Formatar menções
        mencoes = re.findall(r'@(\w+)', texto)
        for username in mencoes:
            texto = texto.replace(f'@{username}', f'<a href="#" class="mention">@{username}</a>')
        
        return texto

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE,  related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="comments_authored")
    conteudo = models.TextField(null=False, blank=False)
    criado_em = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.post_id}"

class Like(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_given")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} likes Post {self.post.post_id}"

class Share(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="shares")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="shares")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shares_made")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} shared Post {self.post.post_id}"

class Reaction(models.Model):
    reaction_id = models.AutoField(primary_key=True, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="reactions")
    post = models.ForeignKey(Comment, on_delete=models.CASCADE,  related_name="reactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="reactions_authored")
    tipo = models.CharField(max_length=50, null=False, blank=False)
    criado_em = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return f"{self.user.username} reacted {self.tipo} on Comment"