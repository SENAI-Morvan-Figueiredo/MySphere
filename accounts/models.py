from django.db import models
from tenants.models import Tenant
from django.contrib.auth.models import AbstractUser, BaseUserManager




class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário precisa de um email")
        email = self.normalize_email(email)

        tenant = extra_fields.pop("tenant", None)
        if tenant and isinstance(tenant, (int, str)):
            tenant = Tenant.objects.get(pk=tenant)

        user = self.model(email=email, tenant=tenant, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa de is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa de is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="tenant")
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    role = models.CharField(max_length=100, null=False, blank=False)
    foto = models.ImageField(upload_to="accounts/", null=True, blank=True)
    data_nascimento = models.DateField(null=False, blank=False)

    objects = UserManager()  

    REQUIRED_FIELDS = ['email', 'role', 'data_nascimento', 'tenant']

    def __str__(self):
        return f"{self.pk}, {self.username}"