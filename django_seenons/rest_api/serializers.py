from rest_framework import serializers

from .models import Customer, Stream, Asset, LogisticServiceProvider, LSPProduct, LSPTimeslot


class CustomerSerializer(serializers.ModelSerializer):
    """ Customer table: contains the data  """

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['id']


class StreamsSerializer(serializers.ModelSerializer):
    """ Serializer for Streams """

    class Meta:
        model = Stream
        fields = '__all__'
        read_only_fields = ['id']


class AssetsSerializer(serializers.ModelSerializer):
    """ Serializer for Assets """

    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['id']


class LogisticServiceProvidersSerializer(serializers.ModelSerializer):
    """ Serializer for LogisticServiceProviders """

    class Meta:
        model = LogisticServiceProvider
        fields = '__all__'
        read_only_fields = ['id']


class LSPProductsSerializer(serializers.ModelSerializer):
    """ Serializer for LSPProducts """

    class Meta:
        model = LSPProduct
        fields = '__all__'
        read_only_fields = ['id']


class WeekdayField(serializers.Field):
    
    WEEKDAYS_MAP = {
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
        0: 'Sunday',
    }

    def to_representation(self, value):
        return self.WEEKDAYS_MAP.get(value, None)

class LSPTimeslotsSerializer(serializers.ModelSerializer):
    """ Serializer for LSPTimeslots """

    # In the form in the DRF GUI, the weekday is a dropdown with weekday names
    weekday = serializers.ChoiceField(list(WeekdayField.WEEKDAYS_MAP.items()))
    
    class Meta:
        model = LSPTimeslot
        fields = '__all__'
        read_only_fields = ['id']
   

class StreamSerializerForProducts(serializers.ModelSerializer):
    """ Serializer for Streams used in ProductsViewSet """

    stream_name = serializers.CharField(source='name')
    availability = LSPTimeslotsSerializer(many=True, read_only=True)
    assets = AssetsSerializer(many=True, read_only=True)

    class Meta:
        model = Stream
        fields = ['id', 'stream_name', 'type', 'availability', 'assets' ]
        read_only_fields = ['id']
