from django.db import models

DIRECTIONS = (
    ('INBOUND', 'Inbound'),
    ('OUTBOUND', 'Outbound')
)


class TickerStation(models.Model):
    id = models.CharField('ID', max_length=10, primary_key=True)

    # Storefront information
    location = models.CharField('Location (store\'s name, etc)', max_length=100)
    address = models.CharField('Address for Location', max_length=100, blank=True)
    contact_notes = models.TextField('Contact details (phone, email, etc) of Location', blank=True)

    # Location information
    latitude = models.FloatField()
    longitude = models.FloatField()

    notes = models.TextField(blank=True)

    def __str__(self):
        return "{} ({})".format(self.id, self.location)


class Prediction(models.Model):
    ticker = models.ForeignKey(TickerStation, on_delete=models.CASCADE)
    route = models.CharField(max_length=4)
    stop_id = models.IntegerField('Stop ID')
    direction = models.CharField(max_length=8, choices=DIRECTIONS)

    def __str__(self):
        return "{} - {}  ({})".format(self.ticker.id, self.route, self.direction)