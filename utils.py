from .models import TickerStation, Prediction
from .settings import API_KEY, API_URL, SEPARATOR

import requests
import xml.etree.ElementTree as ET
from datetime import datetime as dt, timedelta
from django.utils import timezone

ERROR_MESSAGE = "This ticker is experiencing technical difficulties.  Please tweet us to let us know! @twitterhandle"
NO_PREDICTION_MESSAGE =  "{route}({dir}): Too far to predict arrival (>30 mins)"

statuses = {0: 'OK', 10: 'WARNING', 11: "WARNING NO PREDICTION", 20: 'ERROR'}

def get_prediction(prediction):
    dir = "IN" if prediction.direction[0] == 'I' else "OUT"

    off_time = dt.time(21, 30)
    on_time = dt.time(23,30)
    now_time = dt.now().time()
    
    if now_time > off_time and now_time < on_time:
        return '', 11
    
    message, status = "", 20
    # TrueTime request parameters
    params = {
        'key': API_KEY,
        'stpid': prediction.stop_id,
        'rt': prediction.route,
        'dir': prediction.direction,
    }

    # make request to TrueTime API
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:

        results = ET.fromstring(response.text)  # parse the XML response into an ElementTree

        # if no errors
        if not results.findall('error'):
            returned_prediction = results.findall('prd')[0]  # per API: first prediction result == next arrival

            if len(returned_prediction):
                arrival = dt.strptime(returned_prediction.findall('prdtm')[0].text, "%Y%m%d %H:%M")
                time_left = arrival - dt.now() if arrival > dt.now() else timedelta(seconds=0)
                if message in (ERROR_MESSAGE, NO_PREDICTION_MESSAGE):
                    message = ""
                minutes_left = (time_left.seconds / 60)

                message = "{}({}): {} ({:.0f}mins)".format(prediction.route, dir, arrival.strftime('%H:%M'),
                                                           minutes_left)
                status = 0
            else:
                # no predictions often means that a bus isn't coming in the next 30 minutes
                message = NO_PREDICTION_MESSAGE.format(reoute=prediction.route, dir=dir)
                status = 11

        else:
            # Errors from PAT End
            if not message:
                message = NO_PREDICTION_MESSAGE.format(route=prediction.route, dir=dir)
                status = 11
    else:
        # HTTP RESPONSE
        if not message:
            message = ERROR_MESSAGE
            status = 20

    return message, status

def generate_message(ticker):
    # TODO: use redis as message cache
    ticker_id = ticker.id
    predictions = Prediction.objects.filter(ticker=ticker_id)
    messages = []
    final_status = 0
    all_bad = True
    for prediction in predictions:
        msg, status = get_prediction(prediction)

        if status < 20:
            all_bad = False
            messages.append(msg)

        if status > final_status:
            final_status = status

    if not all_bad:
        return SEPARATOR.join(messages) + SEPARATOR, statuses[final_status]
    else:
        return ERROR_MESSAGE, statuses[20]




def collect_message(ticker):
    last_ran = ticker.last_check
    duration = timezone.localtime() - timezone.localtime(last_ran)

    if duration < timezone.timedelta(seconds=45):
        return ticker.last_message, "OK (cached msg)"
    else:
        ticker.last_check=timezone.localtime()
        ticker.save()

        return generate_message(ticker)

