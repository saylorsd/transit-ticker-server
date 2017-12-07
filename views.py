from django.shortcuts import render, get_object_or_404
from .models import TickerStation, Prediction
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict

from .utils import collect_message
from django.utils import timezone


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

def get_message(request, ticker_id=""):
    '''
    Returns message for a particular ticker

    :param request: http request
    :param ticker_id: string - id of ticker
    :return: JsonResponse - containing message
    '''
    success = False
    message = status_msg = ""
    status_code = 400

    
    # get ticker - will raise NotFoundError if bad ticker_id
    ticker = TickerStation.objects.get(pk=ticker_id)

    # get message and/or status
    message, status_msg = collect_message(ticker)
    # TODO: get brightness, speed etc
    status_code = 200
    success = True

    # update status
    ticker.status = status_msg
    ticker.last_message = message
    ticker.save()
    
    response = {'success': success, 'message': message, 'status': status_msg}
    return JsonResponse(response, status=status_code)



