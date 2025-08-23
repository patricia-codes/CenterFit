from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Perfil


# --- Formulário de Registro ---
class UserRegisterForm(UserCreationForm):
  email = forms.EmailField(
    required=True,
    widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-mail"})
  )
  first_name = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Nome'}))
  last_name = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Sobrenome'}))

  cpf = forms.CharField(
    max_length=14,
    widget=forms.TextInput(
    attrs={'class': 'form-control',
           'placeholder':"___.___.___-__",
           'id':'cpf'}))

  class Meta:
    model = User
    fields = ('email', 'first_name', 'last_name', 'cpf', 'password1', 'password2')

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
        raise forms.ValidationError("Este e-mail já está em uso.")
    return email

  def clean_cpf(self):
    cpf = self.cleaned_data.get('cpf')
    # Verifica se já existe CPF cadastrado
    if Perfil.objects.filter(cpf=cpf).exists():
        raise forms.ValidationError("Este CPF já está cadastrado.")
    return cpf

  def save(self, commit=True):
    user = super().save(commit=False)
    user.username = self.cleaned_data['email']
    user.email = self.cleaned_data['email']
    if commit:
      user.save()
      Perfil.objects.create(
          user=user,
          cpf=self.cleaned_data['cpf']
      )
    return user

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
    self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a senha'})

# --- Editar Perfil ---
class UserUpdateForm(UserCreationForm):
  password1 = forms.CharField(
    label="Senha",
    widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Senha"})
  )
  password2 = forms.CharField(
    label="Confirme a senha",
    widget=forms.PasswordInput(
      attrs={"class": "form-control", "placeholder": "Confirme a senha"}))
  cpf = forms.CharField(
    max_length=14,
    widget=forms.TextInput(
    attrs={'class': 'form-control',
           'placeholder':"___.___.___-__",
           'id':'cpf'}))
  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
    widgets = {
      'email': forms.EmailInput(attrs={"class": "form-control-plaintext",
                                      'readonly': 'readolny'}),
      'first_name': forms.TextInput(attrs={"class": "form-control"}),
      'last_name': forms.TextInput(attrs={"class": "form-control"}),
    }
  def __init__(self, *args, **kwargs):
    user = kwargs.get('instance')
    super().__init__(*args, **kwargs)
    # se o user já tem profile, mostrar o cpf no form
    if user and hasattr(user, 'perfil'):
      self.fields['cpf'].initial = user.perfil.cpf

  def clean_email(self):
    email = self.cleaned_data.get('email')
    user = self.instance
    if User.objects.filter(email=email).exclude(pk=user.pk).exists():
      raise forms.ValidationError("Este e-mail já está em uso.")
    return email

  def clean_cpf(self):
    cpf = self.cleaned_data.get('cpf')
    user = self.instance
    # Verifica se já existe CPF cadastrado
    if Perfil.objects.filter(cpf=cpf).exclude(user=user).exists():
      raise forms.ValidationError("Este CPF já está cadastrado.")
    return cpf

  def save(self, commit=True):
    user = super().save(commit=commit)
    cpf = self.cleaned_data.get('cpf')

    if commit:
      profile, created = Perfil.objects.get_or_create(user=user)
      profile.cpf = cpf
      profile.save()

    return user

class CheckoutForm(forms.Form):
  endereco = forms.CharField(
      label="Endereço de entrega",
      widget=forms.TextInput(attrs={
          "class": "form-control",
          "placeholder": "Digite seu endereço completo"
      })
  )

  forma_pagamento = forms.ChoiceField(
      label="Forma de pagamento",
      choices=[
          ("cartao", "Cartão de Crédito"),
          ("boleto", "Boleto"),
          ("pix", "Pix"),
      ],
      widget=forms.Select(attrs={
          "class": "form-select"
      })
  )