from django.http import JsonResponse
from django.shortcuts import render

from app.models import Currency


def today(request):

    rates_data = [[currency.title, currency.from_exchange_rates()] for currency in Currency.objects.all()]

    return render(request, 'rates.html', {
        'rates_data': rates_data
    })


def api(request):
    return JsonResponse({
        'cur': [currency.title for currency in Currency.objects.all()],
        'rates': {
            currency.title: {
                rate.to_currency.title: rate.index for rate in currency.from_exchange_rates()
                }
            for currency in Currency.objects.all()}
    })
