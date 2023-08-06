from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, VerifyForm, AddRecordForm
from .verify import send, check
from .decorators import verification_required
from .models import Record

from django.core.cache import cache
from django.conf import settings


def home(request):
    return render(request, 'home.html', {})


@login_required
@verification_required
# @combined_required
def index(request):
    records = Record.objects.filter(user=request.user)
    return render(request, 'index.html', {'records': records})


def logout_user(request):
    request.user.is_verified = False
    request.user.save()
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect("home")


def password_reset():
    pass


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your registration form has been saved")
            return redirect('login')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


@login_required
def verify_code(request):
    if request.user.is_authenticated:
        user = request.user

        # Rate limiting settings
        rate_limit_key = f'verify_code_attempts:{user.pk}'
        rate_limit_attempts = 3
        rate_limit_duration = 60  # seconds (1 minute)

        if request.method == 'POST':
            form = VerifyForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data.get('code')
                if check(user.phone_number, code):
                    user.is_verified = True
                    user.phone_number_validated = True
                    user.save()
                    return redirect('index')
                else:
                    # Decrement remaining attempts and store in cache
                    remaining_attempts = cache.get(
                        rate_limit_key, rate_limit_attempts)
                    remaining_attempts -= 1
                    cache.set(rate_limit_key, remaining_attempts,
                              rate_limit_duration)

                    if remaining_attempts == 1:
                        messages.error(
                            request, "The code you entered was incorrect. You have 1 more attempt remaining.")
                    else:
                        messages.error(
                            request, f"The code you entered was incorrect. You have {remaining_attempts} attempts remaining.")
            else:
                messages.error(request, "Invalid code. Please try again.")
        else:
            form = VerifyForm()
            phone_number = user.get_phone_number()
            send(phone_number)

        # Get the remaining attempts from cache
        remaining_attempts = cache.get(rate_limit_key, rate_limit_attempts)

        if remaining_attempts <= 0:
            messages.error(
                request, "You have exceeded the permitted number of tries. Please contact our support team to help resolve this issue.")
            return redirect('home')

        return render(request, 'verify.html', {'form': form, 'remaining_attempts': remaining_attempts})
    else:
        return redirect('home')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in")
            user.is_verified = False
            user.save()
            return redirect('verify_code')
        else:
            messages.error(request, "Login failed, please try again")
            return redirect('home')
    return render(request, 'login_user.html', {})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look Up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('index')
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                record = form.save(commit=False)
                record.user = request.user
                record.save()
                messages.success(request, "Record Added...")
                return redirect('index')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('index')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


# def custom_404_page(request, exception):
#     return render(request, '404.html', status=404)
