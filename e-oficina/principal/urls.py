from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from banco import views as banco_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('paginas.urls')), # Home
    
    # Mantem compatibilidade com o que vc ja tinha
    path('banco/', include('banco.urls')),

    # Autenticação (Login/Logout/Cadastro)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', banco_views.signup, name='signup'),

    # Dashboards
    path('painel/cliente/', banco_views.dashboard_cliente, name='dashboard_cliente'),
    path('painel/oficina/', banco_views.dashboard_oficina, name='dashboard_oficina'),
    
    # Ações
    path('servico/<int:pk>/pegar/', banco_views.pegar_servico, name='pegar_servico'),
    path('servico/<int:pk>/concluir/', banco_views.concluir_servico, name='concluir_servico'),
]

# Para servir as imagens enviadas
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)