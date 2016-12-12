from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.shortcuts import render

from app.models import Currency, ExchangeRate, today as date_today


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


def api_history(request):
    pk1 = int(request.GET["pk1"])
    pk2 = int(request.GET["pk2"])
    month_ago = date_today() + relativedelta(months=-1)
    dataPoints = []
    from_currency = Currency.objects.get(id=pk1)
    to_currency = Currency.objects.get(id=pk2)
    labels, data = [], []
    for rate in ExchangeRate.objects.filter(
            from_currency=from_currency,
            to_currency=to_currency,
            date__gte=month_ago
    ).order_by('date'):
        labels.append("{}/{}".format(
            rate.date.day,
            rate.date.month
        ))
        data.append(round(rate.index, 3))
    return JsonResponse({
        'title': "{}/{}".format(
            from_currency,
            to_currency
        ),
        'labels': labels,
        'data': data
    })
