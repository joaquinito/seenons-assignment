from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StreamsSerializer, AssetsSerializer, LogisticServiceProvidersSerializer, LSPProductsSerializer, LSPTimeslotsSerializer
from .models import Streams, Assets, LogisticServiceProviders, LSPProducts, LSPTimeslots


class StreamsViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    serializer_class = StreamsSerializer
    queryset = Streams.objects.all()


class AssetsViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = AssetsSerializer
    queryset = Assets.objects.all()


class LogisticServiceProvidersViewSet(mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      mixins.CreateModelMixin,
                                      mixins.DestroyModelMixin,
                                      viewsets.GenericViewSet):

    serializer_class = LogisticServiceProvidersSerializer
    queryset = LogisticServiceProviders.objects.all()


class LSPProductsViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = LSPProductsSerializer
    queryset = LSPProducts.objects.all()


class LSPTimeslotsViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):

    serializer_class = LSPTimeslotsSerializer
    queryset = LSPTimeslots.objects.all()


class ProductsViewSet(APIView):

    weekday_map = {
        'sunday': 0,
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6,
    }

    def get(self, request):

        postal_code = request.GET.get('postalcode', None)

        try:
            if postal_code is None:
                return Response({'error': 'postalcode is required'}, status=status.HTTP_400_BAD_REQUEST)
            if int(postal_code) < 1000 or int(postal_code) > 9999:
                return Response({'error': 'postalcode must be between 1000 and 9999'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'postalcode must be an integer between between 1000 and 9999'}, status=status.HTTP_400_BAD_REQUEST)

        weekdays_in_params = request.GET.getlist('weekdays', None)
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

        #print(weekdays)
        
        return Response(status=status.HTTP_200_OK)
