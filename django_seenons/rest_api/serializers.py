from rest_framework import serializers

from .models import Customer, Stream, Asset, LogisticServiceProvider, LSPProduct, LSPTimeslot


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


class CustomerSerializer(serializers.ModelSerializer):
    """ Data about Customers """

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['id']


class StreamSerializer(serializers.ModelSerializer):
    """ Data about a Stream """

    class Meta:
        model = Stream
        fields = '__all__'
        read_only_fields = ['id']


class AssetSerializer(serializers.ModelSerializer):
    """ Data about an Asset """

    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['id']


class LogisticServiceProvidersSerializer(serializers.ModelSerializer):
    """ Data about a Logistic Service Provider """

    class Meta:
        model = LogisticServiceProvider
        fields = '__all__'
        read_only_fields = ['id']


class LSPProductSerializer(serializers.ModelSerializer):
    """ Product (Stream + Asset) provided by a Logistic Service Provider """

    class Meta:
        model = LSPProduct
        fields = '__all__'
        read_only_fields = ['id']


class LSPTimeslotSerializer(serializers.ModelSerializer):
    """ Timeslot for a Logistic Service Provider """

    # In the form in the DRF GUI, the weekday is a dropdown with weekday names
    weekday = serializers.ChoiceField(list(WeekdayField.WEEKDAYS_MAP.items()))

    class Meta:
        model = LSPTimeslot
        fields = '__all__'
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    """ Data about product (Stream + Assets) available in a certain area """

    stream_name = serializers.CharField(source='name')
    availability = LSPTimeslotSerializer(many=True, read_only=True)
    assets = AssetSerializer(many=True, read_only=True)

    class Meta:
        model = Stream
        name = 'Products'
        fields = ['id', 'stream_name', 'type', 'availability', 'assets']
        read_only_fields = ['id']
