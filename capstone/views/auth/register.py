import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.urls import reverse
from capstone.models import Customer
from capstone.models import UserType

@csrf_exempt
def register_user(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    '''
    if request.method == "GET":
        template_name = 'auth/register.html'
        return render(request, template_name, {})

    elif request.method == "POST":
        form_data = request.POST

        # Create a new user by invoking the `create_user` helper method
        # on Django's built-in User model
        new_user = User.objects.create_user(
            username=form_data['username'],
            email=form_data['email'],
            password=form_data['password'],
            first_name=form_data['first_name'],
            last_name=form_data['last_name']
        )

        type_of_user = UserType.objects.get(pk=form_data["userType"])

        customer = Customer.objects.create(
            phone_number=form_data['phone_number'],
            address=form_data['address'],
            city=form_data['city'],
            state=form_data['state'],
            zipcode=form_data['zipcode'],
            userType=type_of_user,
            user=new_user
        )

        authenticated_user = authenticate(username=form_data['username'], password=form_data['password'])

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            return redirect(reverse('capstone:home'))

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
