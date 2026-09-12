from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from main.forms.auth import LoginForm, RegisterForm


def _get_safe_next(request):
    redirect_to = request.POST.get('next') or request.GET.get('next') or ''
    if redirect_to and url_has_allowed_host_and_scheme(
        url=redirect_to,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect_to
    return ''


@never_cache
@csrf_protect
def login_view(request):
    """Modern HRMSPro sign-in page."""
    if request.user.is_authenticated:
        return redirect('home')

    next_url = _get_safe_next(request)

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            remember = request.POST.get('remember_me')
            if not remember:
                # Session expires when the browser closes.
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(60 * 60 * 24 * 14)  # 2 weeks
            messages.success(request, f"Welcome back, {user.first_name or user.username}! 👋")
            return redirect(next_url or 'home')
    else:
        form = LoginForm(request)

    return render(request, 'auth/login.html', {'form': form, 'next': next_url})


@never_cache
@csrf_protect
def register_view(request):
    """Modern HRMSPro registration page."""
    if request.user.is_authenticated:
        return redirect('home')

    next_url = _get_safe_next(request)

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(
                request,
                f"Account created successfully. Welcome to HRMSPro, {user.first_name or user.username}! 🎉",
            )
            return redirect(next_url or 'home')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form, 'next': next_url})


@login_required
def logout_view(request):
    """Log the user out (accepts GET for the sidebar link, POST from forms)."""
    auth_logout(request)
    messages.info(request, 'You have been signed out securely. See you soon! 👋')
    return redirect('login')
