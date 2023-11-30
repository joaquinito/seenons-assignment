from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiParameter, extend_schema
from django.core.exceptions import ValidationError

from .serializers import CustomerSerializer, StreamsSerializer, AssetsSerializer, \
    LogisticServiceProvidersSerializer, LSPProductsSerializer, LSPTimeslotsSerializer, \
    StreamSerializerForProducts
from .models import Customer, Stream, Asset, LogisticServiceProvider, LSPProduct, LSPTimeslot


class CustomersViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class StreamsViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    serializer_class = StreamsSerializer
    queryset = Stream.objects.all()


class AssetsViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = AssetsSerializer
    queryset = Asset.objects.all()


class LogisticServiceProvidersViewSet(mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      mixins.CreateModelMixin,
                                      mixins.DestroyModelMixin,
                                      viewsets.GenericViewSet):

    serializer_class = LogisticServiceProvidersSerializer
    queryset = LogisticServiceProvider.objects.all()

    def post(self, request, *args, **kwargs):

        # Check if validation error is raised
        try:
            return self.create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)


class LSPProductsViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = LSPProductsSerializer
    queryset = LSPProduct.objects.all()


class LSPTimeslotsViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):

    serializer_class = LSPTimeslotsSerializer
    queryset = LSPTimeslot.objects.all()


@extend_schema(
    description='Returns all streams available for a given postal code and weekdays, \
                 including the timeslots and assets for each stream.',
    parameters=[
        OpenApiParameter(
                name='postalcode',
                required=True,
                type=int,
                description='Postal code (between 1000 and 9999)',
        ),
        OpenApiParameter(
            name='weekdays',
            required=False,
            description='Weekdays in comma-separated string format \
                         (e.g. "monday", "Tuesday", etc.) or integer format \
                         (0 = Sunday, 1 = Monday, ... 6 = Saturday)',
        ),
    ],
    responses={
        200: StreamSerializerForProducts
    }
)
class ProductsViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    queryset = Stream.objects.all()

    weekdays_map = {
        'sunday': 0,
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6,
    }

    def _validate_postal_code(self, postal_code):
        if postal_code is None:
            raise ValidationError('postalcode is required')
        if not postal_code.isnumeric():
            raise ValidationError(
                'postalcode must be an integer between between 1000 and 9999')
        if int(postal_code) < 1000 or int(postal_code) > 9999:
            raise ValidationError('postalcode must be between 1000 and 9999')

        return True

    def _get_weekdays_id_list(self, weekdays_in_params):
        weekdays = []

        if weekdays_in_params is not None:
            split_elems = weekdays_in_params.split(',')
            for split_elem in split_elems:

                # If string, check if it's a valid weekday name
                if not split_elem.isnumeric():
                    if split_elem.lower() not in self.weekdays_map:
                        raise ValidationError('invalid weekday: ' + split_elem)
                    weekdays.append(self.weekdays_map[split_elem.lower()])

                # If integer, check if it's a valid weekday id
                else:
                    if int(split_elem) < 0 or int(split_elem) > 6:
                        raise ValidationError(
                            'invalid weekday id: ' + split_elem)
                    weekdays.append(int(split_elem))

        return weekdays

    def list(self, request):

        # Get HTTP request parameters
        postal_code = request.GET.get('postalcode', None)
        weekdays_in_params = request.GET.get('weekdays',  None)

        try:
            # Check if postal code is valid
            self._validate_postal_code(postal_code)

            # Check if weekdays are valid and convert to integer-format list
            weekdays = self._get_weekdays_id_list(weekdays_in_params)

        except ValidationError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        # Get all Logistic Service Providers that match the postal code
        lsp_in_postalcode = LogisticServiceProvider.objects.filter(
            postal_code_min__lte=postal_code,
            postal_code_max__gte=postal_code)

        # Get all the Timeslots from those Logistic Service Providers
        lsp_timeslots = LSPTimeslot.objects.filter(
            id_lsp__in=lsp_in_postalcode)
        # Apply weekdays filter to LSP Timeslots
        if len(weekdays) > 0:
            lsp_timeslots = lsp_timeslots.filter(weekday__in=weekdays)

        # Get all LSP Products from all those Logistic Service Providers
        lsp_products = LSPProduct.objects.filter(id_lsp__in=lsp_in_postalcode)

        # Get all the Streams that are in those LSP Products
        streams = self.queryset.filter(
            id__in=lsp_products.values('id_stream'))
        serialized_streams = StreamSerializerForProducts(streams, many=True)

        # Go through all those Streams and add the availability and assets
        filtered_streams = []
        for this_stream in serialized_streams.data:

            # Get the LSPs that have this stream
            lsp_for_this_stream = lsp_in_postalcode.filter(
                id__in=lsp_products.filter(id_stream=this_stream['id']).values('id_lsp'))

            # Get the Timeslots from the LSPs that have this stream
            timeslots_lsp_with_this_stream = lsp_timeslots.filter(
                id_lsp__in=lsp_for_this_stream.values('id'))

            # Add the Timeslots to the stream's availability
            this_stream['availability'] = LSPTimeslotsSerializer(
                timeslots_lsp_with_this_stream, many=True).data

            # Add this stream to our final list if 'availability' is not empty
            if len(this_stream['availability']) != 0:
                filtered_streams.append(this_stream)

            # Get all LSP Products for the selected streams
            products_with_this_stream = lsp_products.filter(
                id_stream=this_stream['id'])

            # Get all Assets for the selected streams
            assets_in_this_stream = Asset.objects.filter(
                id__in=products_with_this_stream.values('id_asset'))

            # Add assets to the stream
            this_stream['assets'] = AssetsSerializer(
                assets_in_this_stream, many=True).data

        return Response(filtered_streams, status=status.HTTP_200_OK)
