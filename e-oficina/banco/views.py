from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Servico, Problema
from .forms import UnifiedSignUpForm, ProblemaForm

# --- Views Antigas (Mantidas) ---
def servico_index(request):
    servicos = Servico.objects.all()
    return render(request, "servico_index.html", {"servicos": servicos})

def servico_detail(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    return render(request, "servico_detail.html", {"servico": servico})

# --- Novas Views do Sistema ---

def signup(request):
    if request.method == 'POST':
        form = UnifiedSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            # --- O SEGREDO ESTÁ AQUI ---
            print("\n====== ERRO NO CADASTRO ======")
            print(form.errors)
            print("==============================\n")
            # ---------------------------
    else:
        form = UnifiedSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
@login_required
def dashboard_cliente(request):
    problemas = Problema.objects.filter(cliente=request.user).order_by('-data_criacao')
    if request.method == 'POST':
        form = ProblemaForm(request.POST, request.FILES)
        if form.is_valid():
            prob = form.save(commit=False)
            prob.cliente = request.user
            prob.save()
            return redirect('dashboard_cliente')
    else:
        form = ProblemaForm()
    return render(request, 'dashboard_cliente.html', {'problemas': problemas, 'form': form})

@login_required
def dashboard_oficina(request):
    disponiveis = Problema.objects.filter(status='ABERTO')
    meus_servicos = Problema.objects.filter(oficina=request.user)
    return render(request, 'dashboard_oficina.html', {
        'disponiveis': disponiveis,
        'meus_servicos': meus_servicos
    })

@login_required
def pegar_servico(request, pk):
    prob = get_object_or_404(Problema, pk=pk)
    if request.user.is_oficina and not prob.oficina:
        prob.oficina = request.user
        prob.status = 'ANDAMENTO'
        prob.save()
    return redirect('dashboard_oficina')

@login_required
def concluir_servico(request, pk):
    prob = get_object_or_404(Problema, pk=pk)
    if prob.oficina == request.user:
        prob.status = 'CONCLUIDO'
        prob.save()
    return redirect('dashboard_oficina')