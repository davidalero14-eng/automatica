from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        if getattr(request.user, 'is_cliente', False):
            return redirect('dashboard_cliente')
        elif getattr(request.user, 'is_oficina', False):
            return redirect('dashboard_oficina')
    return render(request, "home.html", {})