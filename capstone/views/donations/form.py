from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from capstone.models import Company
from capstone.models import Payment

@login_required
def Donation_Form(request):
    companies = Company.objects.all()
    if request.method == 'GET':
        template = 'donations/form.html'

        return render(request, template, {'all_companies': companies})

@login_required
def Donation_Edit_Form(request, donation_id):

    if request.method == 'GET':
        donation = Payment.objects.get(pk=donation_id)

        template = 'donations/form.html'

        return render(request, template, {'form': donation})
