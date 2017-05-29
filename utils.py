from .models import TickerStation, Prediction
from .settings import API_KEY, API_URL

import requests
import xml.etree.ElementTree as ET
from datetime import datetime as dt, timedelta

ERROR_MESSAGE = "This ticker is experiencing technical difficulties.  Please tweet us to let us know! @twitterhandle"
NO_PREDICTION_MESSAGE =  "Zero buses predicted for {route} within next 30 minutes."

def generate_message(ticker):
    # TODO: use redis as message cache
    message = ''
    status = 'ERROR'

    try:
        ticker_id = ticker.id
        predictions = Prediction.objects.filter(ticker=ticker_id)

        for prediction in predictions:

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
                # make a ticker message

                results = ET.fromstring(response.text)      # parse the XML response into an ElementTree

                # if no errors
                if not results.findall('error'):
                    returned_prediction = results.findall('prd')[0]  # per API: first prediction result == next arrival

                    if len(returned_prediction):
                        arrival = dt.strptime(returned_prediction.findall('prdtm')[0].text, "%Y%m%d %H:%M")
                        time = arrival - dt.now()
                        message += "{}: {} ({:.0f}mins) | ".format(prediction.route, arrival.strftime('%H:%M'),
                                                                   (time.seconds / 60))
                        status = "OK"
                    else:
                        # no predictions often means that a bus isn't coming in the next 30 minutes
                        message += NO_PREDICTION_MESSAGE.format(prediction.route)
                        status = "WARNING - NO PREDICTION"

                else:
                    # Errors from PAT End
                    if not message:
                        message = ERROR_MESSAGE
                        status = "ERROR - RESULT ({})".format(results.findall('error')[0].findall('msg')[0].text)
            else:
                # HTTP RESPONSE
                if not message:
                    message =  ERROR_MESSAGE
                    status = "ERROR - HTTP ({})".format(str(response.status_code))

    finally:
        return message, status