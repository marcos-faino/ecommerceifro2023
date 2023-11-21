from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from usuarios.forms import CadUsuarioForm, CadMeuUserForm


class CadUsuarioView(CreateView):
    template_name = 'usuarios/cadusuario.html'
    form_class = CadUsuarioForm

    def form_valid(self, form):
        form.cleaned_data
        grupo = get_object_or_404(Group, name='clientes')
        usuario = form.save()
        usuario.groups.add(grupo)
        usuario.save()
        return redirect('cadmeuusuario', id=usuario.id)

    def form_invalid(self, form):
        print('invalid ', form.cleaned_data)
        messages.error(self.request, 'Usuário não cadastrado!!!')
        return redirect('cadusuario')


class CadMeuUsuarioView(CreateView):
    template_name = 'usuarios/cadmeuusuario.html'
    form_class = CadMeuUserForm
    success_url = reverse_lazy('loginuser')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['usuario'] = User.objects.get(id=self.kwargs['id'])
        return ctx

    def form_valid(self, form):
        meuuser = form.save(commit=False)
        usuario = User.objects.get(id=self.kwargs['id'])
        usuario.email = form.cleaned_data['email']
        usuario.save()
        meuuser.usuario = usuario
        meuuser.save()
        messages.success(self.request, 'Usuario Cadastrado!!!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Usuário não cadastrado!!!')
        print('invalid ', form.cleaned_data)
        return super().form_invalid(form)


class LoginUsuarioView(FormView):
    template_name = 'usuarios/login.html'
    model = User
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        nome = form.cleaned_data['username']
        senha = form.cleaned_data['password']
        usuario = authenticate(self.request,username=nome, password=senha)
        if usuario is not None:
            login(self.request, usuario)
            return redirect('listarprod')
        messages.error(self.request, 'Usuário inexistente.')
        return redirect('loginuser')

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível logar!')
        return redirect('loginuser')


class LogoutView(LoginRequiredMixin, LogoutView):

    def get(self, request):
        logout(request)
        return redirect('home')
