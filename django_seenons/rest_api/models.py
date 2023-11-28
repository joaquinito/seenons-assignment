from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Streams(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    details_url = models.CharField(max_length=300, null=True)
    image_url = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name


class Assets(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=200)
    sub_category = models.CharField(max_length=200)
    size = models.IntegerField()
    size_unit = models.CharField(max_length=200)
    image_url = models.CharField(max_length=300, null=True)
    placement_type = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category + ' - ' + self.sub_category + ' - ' + str(self.size) + ' ' + self.size_unit


class LogisticServiceProviders(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    postal_code_min = models.IntegerField()
    postal_code_max = models.IntegerField()

    def __str__(self):
        return self.name + ' (' + str(self.postal_code_min) + '-' + str(self.postal_code_max) + ')'


class LSPProducts(models.Model):
    id = models.AutoField(primary_key=True)
    id_lsp = models.ForeignKey(
        LogisticServiceProviders, on_delete=models.CASCADE)
    id_stream = models.ForeignKey(Streams, on_delete=models.CASCADE)
    id_asset = models.ForeignKey(Assets, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_lsp.name + ' - ' + self.id_stream.name + ' - ' + self.id_asset.category


class LSPTimeslots(models.Model):
    id = models.AutoField(primary_key=True)
    id_lsp = models.ForeignKey(
        LogisticServiceProviders, on_delete=models.CASCADE)
    weekday = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(6)])
    every_other_week = models.BooleanField()
    timeslot_start = models.TimeField(null=True)
    timeslot_end = models.TimeField(null=True)

    def __str__(self):
        return self.id_lsp.name + ' - ' + str(self.weekday) + ' - ' + str(self.timeslot_start) + ' - ' + str(self.timeslot_end)
