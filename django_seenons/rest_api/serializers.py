
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

    WEEKDAY_CHOICES = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (0, 'Sunday'),
    )

    weekday = serializers.SerializerMethodField()

    class Meta:
        model = LSPTimeslots
        fields = '__all__'
        read_only_fields = ['id']

    def get_weekday(self, obj):
        return self.WEEKDAY_CHOICES[obj.weekday][1]


class StreamSerializerForProducts(serializers.ModelSerializer):
    """ Serializer for Streams used in ProductsViewSet """
    stream_name = serializers.CharField(source='name')

    class Meta:
        model = Streams
        fields = ['id', 'stream_name', 'type', 'details_url', 'image_url']
        read_only_fields = ['id']
