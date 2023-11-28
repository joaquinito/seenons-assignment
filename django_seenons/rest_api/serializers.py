
from rest_framework import serializers
from .models import Streams


class StreamsSerializer(serializers.ModelSerializer):
    """ Serializer for Streams """

    class Meta:
        model = Streams
        fields = ['id', 'name', 'type', 'details_url', 'image']
        read_only_fields = ['id']


