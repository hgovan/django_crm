from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, VerifyForm
from .verify import send, check
from .decorators import verification_required


def home(request):
    return render(request, 'home.html', {})


@login_required
@verification_required
# @combined_required
def index(request):
    print("in")
    return render(request, 'index.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    request.user.is_verified = False
    return redirect("home")


def password_reset():
    pass


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your registration form has been saved")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            send(form.cleaned_data['phone'])
            return login_user(request, user)
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


@login_required
def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if check(request.user.phone_number, code):
                request.user.is_verified = True
                request.user.save()
                print("verify_code")
                return redirect('index')
            else:
                return redirect('home')
    else:
        form = VerifyForm()
    return render(request, 'verify.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in")
            # phone_number = user.get_phone_number()
            # send(phone_number)
            return redirect('verify_code')
        else:
            messages.error(request, "Login failed, please try again")
            return redirect('home')
    return render(request, 'login_user.html', {})


def custom_404_page(request, exception):
    return render(request, '404.html', status=404)
