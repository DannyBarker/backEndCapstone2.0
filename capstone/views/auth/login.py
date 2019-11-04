from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib import messages

def login_user(request):
    if request.method == "GET":
        template_name = 'donations/form.html'
        return render(request, template_name, {})

    elif request.method == "POST":
        form_data = request.POST
        authenticated_user = authenticate(username=form_data['username'], password=form_data['password'])

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            return redirect(reverse('capstone:donation_form'))

        else:
            # Bad login details were provided. So we can't log the user in.
            # print("Invalid login details: {}, {}".format(form_data['username'], password=form_data['password']))
            return HttpResponse(status=204)