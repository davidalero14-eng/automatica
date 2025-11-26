from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Problema

class UnifiedSignUpForm(UserCreationForm):
    TIPO_CHOICES = (
        ('CLIENTE', 'Sou Cliente'),
        ('OFICINA', 'Sou Oficina'),
    )
    tipo_usuario = forms.ChoiceField(choices=TIPO_CHOICES, widget=forms.RadioSelect, label="Tipo de Conta")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['tipo_usuario'] == 'CLIENTE':
            user.is_cliente = True
        else:
            user.is_oficina = True
        if commit:
            user.save()
        return user

class ProblemaForm(forms.ModelForm):
    class Meta:
        model = Problema
        fields = ['titulo', 'modelo_carro', 'descricao', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo_carro': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }