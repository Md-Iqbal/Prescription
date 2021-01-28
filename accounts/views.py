from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

#login, registration

def registerView(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/patient')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'login.html', context)

def logoutView(request):
    logout(request)
    return redirect('login')

class password_change(TemplateView):
    template_name = "password_change.html"

    def post(self, request):
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user = request.user)
            messages.success(request, "Password changed successfully!!!")
            return redirect('login')
        else:
            messages.error(request, "Password did not matched!")
            return redirect("/changePaSs")

    def get(self, request):
        form = PasswordChangeForm(user = request.user)
        return render(request, self.template_name, {"form":form})
#non-registered user

class indexView(TemplateView):
    template_name = "index.html"


class serviceView(TemplateView):
    template_name = "service.html"


class adviceView(TemplateView):
    template_name = "advice.html"


class aboutUSView(TemplateView):
    template_name = "about.html"


class contactView(TemplateView):
    template_name = "contact.html"


class Documentation(TemplateView):
    template_name = "documentation.html"
