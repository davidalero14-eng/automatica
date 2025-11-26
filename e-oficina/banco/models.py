from django.db import models
from django.contrib.auth.models import AbstractUser

# --- Mantendo o antigo para não perder compatibilidade ---
class Servico(models.Model):
    carro = models.CharField(max_length=100)
    imagem = models.TextField()
    tipo = models.CharField(max_length=20)
    def __str__(self): return self.carro

# --- NOVOS MODELOS NECESSÁRIOS ---

class User(AbstractUser):
    is_cliente = models.BooleanField(default=False)
    is_oficina = models.BooleanField(default=False)

class Problema(models.Model):
    STATUS_CHOICES = (
        ('ABERTO', 'Em Aberto'),
        ('ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDO', 'Concluído'),
    )
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problemas_criados')
    oficina = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicos_pegos')
    
    titulo = models.CharField(max_length=200)
    modelo_carro = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='problemas/', blank=True, null=True)
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')

    def __str__(self):
        return f"{self.modelo_carro} - {self.titulo}"