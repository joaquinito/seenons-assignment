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
        
        ## Check if validation error is raised
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
    description='Returns all products available for a given postal code and weekdays',
    parameters=[
        OpenApiParameter(
                name='postalcode',
                required=True,
                type=int,
                description='Postal code of the customer',
        ),
    ],
)
class ProductsViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    queryset = Stream.objects.all()

    weekday_map = {
        'sunday': 0,
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6,
    }

    def list(self, request):

        # Get request parameters
        postal_code = request.GET.get('postalcode', None)
        weekdays_in_params = request.GET.getlist('weekdays', None)

        # Check if postal code is valid
        try:
            if postal_code is None:
                return Response({'error': 'postalcode is required'},
                                status=status.HTTP_400_BAD_REQUEST)
            if int(postal_code) < 1000 or int(postal_code) > 9999:
                return Response({'error': 'postalcode must be between 1000 and 9999'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'postalcode must be an integer between between 1000 and 9999'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Get weekdays in integer format from request parameters
        weekdays = []
        if weekdays_in_params is not None:
            for elem in weekdays_in_params:

                # TODO: Clean this up, create a new function to add to weekdays list
                if ',' in elem:
                    split_elems = elem.split(',')

                    for split_elem in split_elems:
                        if not split_elem.isnumeric():
                            weekdays.append(
                                self.weekday_map[split_elem.lower()])
                        else:
                            weekdays.append(int(split_elem))

                elif not elem.isnumeric():
                    weekdays.append(self.weekday_map[elem.lower()])
                else:
                    weekdays.append(int(elem))

         # Get all Logistic Service Providers that match the postal code
        lsp_in_postalcode = LogisticServiceProvider.objects.filter(
            postal_code_min__lte=postal_code,
            postal_code_max__gte=postal_code)

        # Get all LSP Timeslots for the Logistic Service Providers
        lsp_timeslots = LSPTimeslot.objects.filter(
            id_lsp__in=lsp_in_postalcode)
        # Apply weekdays filter to LSP Timeslots
        if len(weekdays) > 0:
            lsp_timeslots = lsp_timeslots.filter(weekday__in=weekdays)
        serialized_lsp_timeslots = LSPTimeslotsSerializer(
            lsp_timeslots, many=True)
        
        # Get all LSP Products from all the Logistic Service Providers in that postal code
        lsp_products = LSPProduct.objects.filter(id_lsp__in=lsp_in_postalcode)

        # Get all the Streams that are in those LSP Products
        streams = Stream.objects.filter(
            id__in=lsp_products.values('id_stream'))
        serialized_streams = StreamSerializerForProducts(streams, many=True)

        filtered_streams = []
        # Add assets and availability to each stream
        for each_stream in serialized_streams.data:

            each_stream['availability'] = serialized_lsp_timeslots.data
            # Remove each_stream from the serialized_streams.data list if 'availability' is empty
            if len(each_stream['availability']) != 0:
                filtered_streams.append(each_stream)

            # Get all LSP Products for the selected streams
            products_with_this_stream = lsp_products.filter(
                id_stream=each_stream['id'])
            assets_in_this_stream = Asset.objects.filter(
                id__in=products_with_this_stream.values('id_asset'))
            each_stream['assets'] = AssetsSerializer(
                assets_in_this_stream, many=True).data

        return Response(filtered_streams, status=status.HTTP_200_OK)
