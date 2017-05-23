# settings-example.py
#
# !! IMPORTANT - rename this file to settings.py and chang `API_KEY` to your API key !!
#


API_KEY = "YOUR_API_KEY_HERE!"              # TrueTime API key from Port Authority
API_URL = 'http://realtime.portauthority.org/bustime/api/v1/getpredictions'

# Default ticker paramters
DEFAULT_DURATION = 30                       # Number of minutes you want it to run for
DEFAULT_WIDTH = 4                           # Width of ticker (i.e. number of matrices)
DEFAULT_BRIGHTNESS = 1                      # LED brightness: 0-15
DEFAULT_SPEED = 5                           # Message speed 1-10
DEFAULT_SCROLL_TIMES = 10                   # number of times to scroll message before checking for new times
