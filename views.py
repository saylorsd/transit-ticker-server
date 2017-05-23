from django.shortcuts import render, get_object_or_404
from .models import TickerStation, Prediction
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict

def index(request):
    pass


def get_tickers(request):
    """
    Get information on all tickers

    :param request:
    :return:
    """

    resp = {'success': True, 'results': list(TickerStation.objects.values())}
    return JsonResponse(resp)

def get_ticker(request, ticker_id=""):
    """
    Get information on specific ticker station.

    :param request: http request
    :param ticker_id: id of ticker
    :return: JsonResponse - data representing ticker
    """
    # Returns requested ticker
    try:
        ticker = TickerStation.objects.get(pk=ticker_id)
        data = model_to_dict(ticker)
        resp = {'success': True, 'results': data}
    except:
        resp = {'success': False, 'results': {}, 'help': 'Ticker ({}) not found.'.format(ticker_id)}


    return JsonResponse(resp)


def get_message(request, ticker_id):
    pass

def get_status(request, ticker_id):
    pass

