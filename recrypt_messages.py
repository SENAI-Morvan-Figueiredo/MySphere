import os
import django
from cryptography.fernet import Fernet

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MySphere.settings")  # ajuste o nome do seu projeto
django.setup()

from chat.models import Message

# 🔑 Substitua aqui
FERNET_KEY_OLD = b"7UU5gjQ7pT3Jzitp7pWh3_tyHoPbtnG94zeJPOaGI0k="
FERNET_KEY_NEW = b"UxvMeubPXqjbKLyP_Ky199lE9Bns0Nj3AoQTVlHA_F8="

fernet_old = Fernet(FERNET_KEY_OLD)
fernet_new = Fernet(FERNET_KEY_NEW)

recriptografadas = 0
falhas = 0

for msg in Message.objects.all():
    try:
        texto_original = fernet_old.decrypt(bytes(msg.conteudo_encrypted)).decode()
        msg.conteudo_encrypted = fernet_new.encrypt(texto_original.encode())
        msg.save(update_fields=["conteudo_encrypted"])
        recriptografadas += 1
    except Exception as e:
        falhas += 1
        print(f"❌ Falha ao processar msg {msg.id}: {e}")

print(f"\n✅ Mensagens recriptografadas: {recriptografadas}")
print(f"⚠️ Falhas: {falhas}")
