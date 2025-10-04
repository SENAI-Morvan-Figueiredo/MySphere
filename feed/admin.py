from django.contrib import admin
from .models import Post, Comment, Reaction, Like, Share

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Share)
admin.site.register(Reaction)
