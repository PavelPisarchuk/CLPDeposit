from django.shortcuts import render


def today(request):
    from app.models import Currency

    rates_data = [[currency.title, currency.from_exchange_rates()] for currency in Currency.objects.all()]

    return render(request, 'rates.html', {
        'rates_data': rates_data
    })
