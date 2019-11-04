from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from capstone.models import Payment
from capstone.models import GiftCard
from capstone.models import Customer
from capstone.models import Company
import datetime



@login_required
def Donation_List(request):
    user = request.user
    current_customer = Customer.objects.get(pk=user.id)

    if request.method == 'GET':
        total_donated = 0

        try:
            user_donations = current_customer.donations.all()
        except Payment.DoesNotExist:
            user_donations = []

        for donation in user_donations:
            total_donated += float(donation.amount_donated)

        template_name = "donations/list.html"
        return render(request, template_name, {'all_donations': user_donations, "total_donated": total_donated, "user_name": user.first_name})

    elif request.method == 'POST':
        form_data = request.POST
        companies = Company.objects.all()
        company_name = companies.get(pk=form_data["company_card_name"])

        try:
            new_card = GiftCard.objects.get(company__id=form_data["company_card_name"], barcode=form_data["barcode"])

            if new_card.remaining_balance > 0.00:
                new_payment = Payment.objects.create(
                payment_date=datetime.date.today(),
                customer=current_customer,
                giftcard=new_card,
                amount_donated=new_card.remaining_balance
                )
                if form_data["description"] != "":
                    new_card.description = form_data["description"]
                    new_card.save()

                new_card.remaining_balance = new_card.remaining_balance - new_payment.amount_donated
                new_card.save()

                return redirect(reverse('capstone:donations'))
            else:
                messages.info(request, f"The {company_name.name} card has no remaining balance to give!")

                return render(request, "donations/form.html",{"form": form_data, "all_companies": companies})
        except GiftCard.DoesNotExist:
            company_name = companies.get(pk=form_data["company_card_name"])
            messages.info(request, f"Could not find the {company_name.name} card!")

            return render(request, "donations/form.html",{"form": form_data, "all_companies": companies})
