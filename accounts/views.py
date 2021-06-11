from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import UpdateView

from .forms import SignUpForm

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    labels = {
        'first_name' : 'Nome',
        'last_name' : 'Sobrenome'
    }
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user

def home(request):
    return render(request,'accounts/index.html', {})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(reverse('pecas:index'))
    else:
        form = SignUpForm()
    return render(request,'accounts/signup.html', {'form': form})


