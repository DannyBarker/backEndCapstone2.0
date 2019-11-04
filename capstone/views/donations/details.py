from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from capstone.models import Payment


@login_required
def Donation_Details(request, donation_id):
    donation = Payment.objects.get(pk=donation_id)
    if request.method == 'GET':
        template_name = 'donations/details.html'
        return render(request, template_name, {'donation': donation})

    elif request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for editing a book
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            if form_data["description"] != "":
                donation.description = form_data["description"]
            else:
                donation.description = "I donated!"


            donation.save()

            return redirect(reverse('capstone:donations'))