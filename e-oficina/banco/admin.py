from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Problema, Servico

# Configura o Admin para o seu Usuário Personalizado
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Tipo de Usuário', {'fields': ('is_cliente', 'is_oficina')}),
    )
    list_display = ['username', 'email', 'is_cliente', 'is_oficina', 'date_joined']
    list_filter = ['is_cliente', 'is_oficina']

# Registra os outros modelos para você ver também
@admin.register(Problema)
class ProblemaAdmin(admin.ModelAdmin):
    list_display = ('modelo_carro', 'titulo', 'cliente', 'oficina', 'status')
    list_filter = ('status',)

admin.site.register(Servico) # Seu modelo antigo