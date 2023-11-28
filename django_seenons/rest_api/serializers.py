
from rest_framework import serializers
from .models import Streams, Assets, LogisticServiceProviders, LSPProducts, LSPTimeslots


class StreamsSerializer(serializers.ModelSerializer):
    """ Serializer for Streams """

    class Meta:
        model = Streams
        fields = '__all__'
        read_only_fields = ['id']


class AssetsSerializer(serializers.ModelSerializer):
    """ Serializer for Assets """

    class Meta:
        model = Assets
        fields = '__all__'
        read_only_fields = ['id']


class LogisticServiceProvidersSerializer(serializers.ModelSerializer):
    """ Serializer for LogisticServiceProviders """

    class Meta:
        model = LogisticServiceProviders
        fields = '__all__'
        read_only_fields = ['id']


class LSPProductsSerializer(serializers.ModelSerializer):
    """ Serializer for LSPProducts """

    class Meta:
        model = LSPProducts
        fields = '__all__'
        read_only_fields = ['id']


class LSPTimeslotsSerializer(serializers.ModelSerializer):
    """ Serializer for LSPTimeslots """

    class Meta:
        model = LSPTimeslots
        fields = '__all__'
        read_only_fields = ['id']

    