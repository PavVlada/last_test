from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('publications')
    

class RegisterPage(FormView):
    template_name = 'user/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('publications')

    def form_valid(self, form) -> HttpResponse:
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('publications')
        return super(RegisterPage, self).get(*args, **kwargs)
