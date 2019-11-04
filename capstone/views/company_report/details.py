from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from capstone.models import Payment
from capstone.models import Customer

def make_report(company_id):
    company_area_report = dict()
    overall_report = dict()
    overall_report["payments"] = Payment.objects.all().filter(giftcard__company__id=company_id)
    overall_report["total"] = 0

    for payment in overall_report["payments"]:
        if str(payment.customer.zipcode) not in company_area_report:
            company_area_report[f"{payment.customer.zipcode}"] = payment.amount_donated
        else:
            company_area_report[f"{payment.customer.zipcode}"] += payment.amount_donated

    for k,v in company_area_report.items():
        overall_report["total"] += v

    overall_report["zipcodes"] = company_area_report
    overall_report["company_id"] = company_id

    return overall_report

@login_required
def Report_Details(request):
    customer = Customer.objects.get(pk=request.user.id)
    company_id = customer.company.id
    if request.method == 'GET':
        company_report = make_report(company_id)
        template_name = 'report/details.html'
        return render(request, template_name, company_report)

    # elif request.method == 'POST':
    #     form_data = request.POST

    #     # Check if this POST is for editing a book
    #     if (
    #         "actual_method" in form_data
    #         and form_data["actual_method"] == "PUT"
    #     ):
    #         if form_data["description"] != "":
    #             donation.description = form_data["description"]
    #         else:
    #             donation.description = "I donated!"


    #         donation.save()

    #         return redirect(reverse('capstone:donations'))