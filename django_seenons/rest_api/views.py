from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_api import serializers
from rest_api.models import Streams


class StreamsViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
   
    serializer_class = serializers.StreamsSerializer
    queryset = Streams.objects.all()