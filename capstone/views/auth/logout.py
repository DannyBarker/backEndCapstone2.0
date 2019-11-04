from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout

@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse('capstone:home'))