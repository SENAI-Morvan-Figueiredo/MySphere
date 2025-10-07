from django.contrib import admin
from .models import Chat, Message, Contact

# -------------------------
# Admin de Contact
# -------------------------
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact', 'tenant', 'aceito')
    list_filter = ('tenant', 'aceito')
    search_fields = ('user__username', 'contact__username')

# -------------------------
# Admin de Chat
# -------------------------
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user1', 'user2', 'tenant', 'criado_em')
    list_filter = ('tenant', 'criado_em')
    search_fields = ('user1__username', 'user2__username')
    readonly_fields = ('criado_em',)

# -------------------------
# Admin de Message
# -------------------------
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'remetente', 'conteudo_texto', 'lido', 'criado_em')
    list_filter = ('chat', 'remetente', 'lido', 'criado_em')
    search_fields = ('remetente__username', 'chat__user1__username', 'chat__user2__username')
    readonly_fields = ('criado_em', 'conteudo_texto')

    # Método para exibir o conteúdo descriptografado
    def conteudo_texto(self, obj):
        try:
            return obj.conteudo
        except Exception:
            return "[Erro ao descriptografar]"
    conteudo_texto.short_description = "Conteúdo"
