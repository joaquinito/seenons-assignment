from django.db import models
from datetime import timedelta, datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Customer(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    postal_code = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)])

    def __str__(self):
        return self.name


class Stream(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Asset(models.Model):

    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=200)
    sub_category = models.CharField(max_length=200)
    size = models.PositiveIntegerField(default=0)
    size_unit = models.CharField( max_length=200)
    image_url = models.CharField(null=True, max_length=300, )
    placement_type = models.CharField(max_length=200)

    def __str__(self):
        return self.category + ' - ' + self.sub_category + ' - ' +\
            str(self.size) + ' ' + self.size_unit


class LogisticServiceProvider(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    postal_code_min = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    postal_code_max = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)])

    def save(self, *args, **kwargs):
        if self.postal_code_min > self.postal_code_max:
            raise ValidationError('Postal Code Max must be equal to or greater than Postal Code Min')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name + ' (' + str(self.postal_code_min) + '-' +\
            str(self.postal_code_max) + ')'


class LSPProduct(models.Model):

    id = models.AutoField(primary_key=True)
    id_lsp = models.ForeignKey(
        LogisticServiceProvider, on_delete=models.CASCADE)
    id_stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    id_asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_lsp.name + ' - ' + self.id_stream.name + ' - ' +\
            self.id_asset.category


class LSPTimeslot(models.Model):

    id = models.AutoField(primary_key=True)
    id_lsp = models.ForeignKey(
        LogisticServiceProvider, on_delete=models.CASCADE)
    weekday = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(6)])
    every_other_week = models.BooleanField()
    timeslot_start = models.TimeField(
        null=True,
        validators=[MinValueValidator(datetime(1, 1, 1, 6, 0, 0).time(),
                                      message='Timeslot start must be between 06:00 and 20:00'),
                    MaxValueValidator(datetime(1, 1, 1, 20, 0, 0).time(),
                                      message='Timeslot start must be between 06:00 and 20:00')])
    timeslot_end = models.TimeField(null=True, editable=False)

    # timeslot_end is automatically added based on timeslot_start
    # - it will be 2 hours later
    def save(self, *args, **kwargs):
        if self.timeslot_start is not None:
            start_datetime = datetime.combine(
                datetime(1, 1, 1), self.timeslot_start)
            self.timeslot_end = (start_datetime + timedelta(hours=2)).time()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id_lsp.name + ' - ' + str(self.weekday) + ' - ' +\
            str(self.timeslot_start) + ' - ' + str(self.timeslot_end)
