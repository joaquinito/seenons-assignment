from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from datetime import datetime
from rest_framework.test import APIRequestFactory
from .views import ProductsViewSet
from .models import LogisticServiceProvider, Stream, Asset, LSPProduct, LSPTimeslot


class ProductsAPITestCase(TestCase):
    """ Tests for the endpoint GET /api/products/ """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProductsViewSet.as_view({'get': 'list'})
        self.uri = '/api/products/'

        # Logistic Service Providers
        self.lsp_1000_2000 = LogisticServiceProvider.objects.create(
            name='LSP-1000-2000',
            postal_code_min='1000',
            postal_code_max='2000',
        )
        self.lsp_1000_1100 = LogisticServiceProvider.objects.create(
            name='LSP-1000-1100',
            postal_code_min='1000',
            postal_code_max='1100',
        )
        self.lsp_1000_1050 = LogisticServiceProvider.objects.create(
            name='LSP-1000-1050',
            postal_code_min='1000',
            postal_code_max='1050',
        )

        # Streams
        self.stream_a = Stream.objects.create(
            name='Stream A',
            type='Type A',
        )

        self.stream_b = Stream.objects.create(
            name='Stream B',
            type='Type B',
        )

        self.stream_c = Stream.objects.create(
            name='Stream C',
            type='Type C',
        )

        # Assets
        self.asset_alpha = Asset.objects.create(
            category='Category Alpha',
            sub_category='Subcategory Alpha',
            size='100',
            size_unit='Unit Alpha',
            placement_type='Type Alpha',
        )

        self.asset_beta = Asset.objects.create(
            category='Category Beta',
            sub_category='Subcategory Beta',
            size='200',
            size_unit='Unit Beta',
            placement_type='Type Beta',
        )

        self.asset_gamma = Asset.objects.create(
            category='Category Gamma',
            sub_category='Subcategory Gamma',
            size='300',
            size_unit='Unit Gamma',
            placement_type='Type Gamma',
        )

        self.asset_delta = Asset.objects.create(
            category='Category Delta',
            sub_category='Subcategory Delta',
            size='400',
            size_unit='Unit Delta',
            placement_type='Type Delta',
        )

        self.asset_epsilon = Asset.objects.create(
            category='Category Epsilon',
            sub_category='Subcategory Epsilon',
            size='500',
            size_unit='Unit Epsilon',
            placement_type='Type Epsilon',
        )

        # LSPProducts
        self.lsp_product_1000_1050_a_alpha = LSPProduct.objects.create(
            id_lsp=self.lsp_1000_1050,
            id_stream=self.stream_a,
            id_asset=self.asset_alpha,
        )

        self.lsp_product_1000_1050_a_beta = LSPProduct.objects.create(
            id_lsp=self.lsp_1000_1050,
            id_stream=self.stream_a,
            id_asset=self.asset_beta,
        )

        self.lsp_product_3_1000_1100_a_beta = LSPProduct.objects.create(
            id_lsp=self.lsp_1000_1100,
            id_stream=self.stream_a,
            id_asset=self.asset_beta,
        )

        self.lsp_product_1000_1100_a_gamma = LSPProduct.objects.create(
            id_lsp=self.lsp_1000_1100,
            id_stream=self.stream_a,
            id_asset=self.asset_gamma,
        )

        self.lsp_product_1000_1100_b_delta = LSPProduct.objects.create(
            id_lsp=self.lsp_1000_1100,
            id_stream=self.stream_b,
            id_asset=self.asset_delta,
        )

        self.lsp_product_1000_1100_b_epsilon = LSPProduct.objects.create(
            id_lsp=self.lsp_1000_1100,
            id_stream=self.stream_b,
            id_asset=self.asset_epsilon,
        )

        self.lsp_product_1000_2000_c_alpha = LSPProduct.objects.create(
            id_lsp=self.lsp_1000_2000,
            id_stream=self.stream_c,
            id_asset=self.asset_alpha,
        )

        # LSPTimeslots
        self.lsp_timeslot_1000_1050_monday_14 = LSPTimeslot.objects.create(
            id_lsp=self.lsp_1000_1050,
            weekday=1,
            every_other_week=False,
            timeslot_start=datetime(1, 1, 1, 14, 0, 0).time(),
            timeslot_end=datetime(1, 1, 1, 16, 0, 0).time(),
        )

        self.lsp_timeslot_1000_1050_tuesday_10 = LSPTimeslot.objects.create(
            id_lsp=self.lsp_1000_1050,
            weekday=2,
            every_other_week=False,
            timeslot_start=datetime(1, 1, 1, 10, 0, 0).time(),
            timeslot_end=datetime(1, 1, 1, 12, 0, 0).time(),
        )

        self.lsp_timeslot_1000_1050_wednesday_10 = LSPTimeslot.objects.create(
            id_lsp=self.lsp_1000_1050,
            weekday=3,
            every_other_week=True,
            timeslot_start=datetime(1, 1, 1, 10, 0, 0).time(),
            timeslot_end=datetime(1, 1, 1, 12, 0, 0).time(),
        )

        self.lsp_timeslot_1000_1100_wednesday_16 = LSPTimeslot.objects.create(
            id_lsp=self.lsp_1000_1100,
            weekday=3,
            every_other_week=False,
            timeslot_start=datetime(1, 1, 1, 16, 0, 0).time(),
            timeslot_end=datetime(1, 1, 1, 18, 0, 0).time(),
        )

        self.lsp_timeslot_1000_1100_thursday_17 = LSPTimeslot.objects.create(
            id_lsp=self.lsp_1000_1100,
            weekday=4,
            every_other_week=False,
            timeslot_start=datetime(1, 1, 1, 17, 0, 0).time(),
            timeslot_end=datetime(1, 1, 1, 19, 0, 0).time(),
        )

        self.lsp_timeslot_1000_2000_monday_11 = LSPTimeslot.objects.create(
            id_lsp=self.lsp_1000_2000,
            weekday=1,
            every_other_week=False,
            timeslot_start=datetime(1, 1, 1, 11, 0, 0).time(),
            timeslot_end=datetime(1, 1, 1, 13, 0, 0).time(),
        )

        self.lsp_timeslot_1000_2000_friday_8 = LSPTimeslot.objects.create(
            id_lsp=self.lsp_1000_2000,
            weekday=5,
            every_other_week=False,
            timeslot_start=datetime(1, 1, 1, 8, 0, 0).time(),
            timeslot_end=datetime(1, 1, 1, 10, 0, 0).time(),
        )

    # --------------------------------------------------------------------------------------------
    # TEST NEG: If no postalcode is provided, it should return 400 Bad Request.
    def test_get_products_without_postalcode(self):

        # Get API response
        response = self.client.get(reverse('rest_api:products-list'))
        # Check that status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Message should be 'postalcode is required'
        self.assertEqual(response.data['error'], 'postalcode is required')

    # --------------------------------------------------------------------------------------------
    # TEST NEG: If postalcode provided is out of range , it should return 400 Bad Request.
    def test_get_products_with_postalcode_out_of_range(self):

        # Get API response
        response = self.client.get(
            reverse('rest_api:products-list'), {'postalcode': '12345'})
        # Check that status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Message should be 'postalcode is required'
        self.assertEqual(response.data['error'],
                         'postalcode must be between 1000 and 9999')

    # --------------------------------------------------------------------------------------------
    # TEST NEG: If postalcode provided is not an integer, it should return 400 Bad Request.
    def test_get_products_with_postalcode_not_integer(self):

        # Get API response
        response = self.client.get(
            reverse('rest_api:products-list'), {'postalcode': 'abc'})
        # Check that status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Message should be 'postalcode is required'
        self.assertEqual(
            response.data['error'], 'postalcode must be an integer between 1000 and 9999')

    # --------------------------------------------------------------------------------------------
    # TEST POS: Get correct response without weekdays filter.
    #
    # For postalcode 1000, it should return the following products:
    # - Stream A, Assets alpha and beta and gamma, timeslots Monday 14:00, Tuesday 10:00,
    #     Wednesday 10:00, Wednesday 16:00, Thursday 17:00
    # - Stream B, Assets delta and epsilon, timeslots Wednesday 16:00, Thursday 17:00
    # - Stream C, Assets alpha, timeslots Monday 11:00, Friday 8:00
    def test_get_products_with_postalcode_1000(self):

        # Get API response
        response = self.client.get(
            reverse('rest_api:products-list'), {'postalcode': '1000'})
        # Check that status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extract the json from the response
        response_data = response.json()
        # Check that the number of products is correct
        self.assertEqual(len(response_data), 3)

        # Check that the first stream is correct
        self.assertEqual(response_data[0]['stream_name'], 'Stream A')
        # Check that the first stream has 5 timeslots
        self.assertEqual(len(response_data[0]['availability']), 5)
        # Check that the first stream has 3 assets
        self.assertEqual(len(response_data[0]['assets']), 3)

        # Check that the second stream is correct
        self.assertEqual(response_data[1]['stream_name'], 'Stream B')
        # Check that the second stream has 2 timeslots
        self.assertEqual(len(response_data[1]['availability']), 2)
        # Check that the second stream has 2 assets
        self.assertEqual(len(response_data[1]['assets']), 2)

        # Check that the third stream is correct
        self.assertEqual(response_data[2]['stream_name'], 'Stream C')
        # Check that the third stream has 2 timeslots
        self.assertEqual(len(response_data[2]['availability']), 2)
        # Check that the third stream has 1 asset
        self.assertEqual(len(response_data[2]['assets']), 1)

    # --------------------------------------------------------------------------------------------
    # TEST POS: Correct response with weekdays filter.
    #
    # For postalcode 1000 on weekeday Monday, it should return the following products:
    # - Stream A, Assets alpha and beta, timeslots Monday 14:00
    # - Stream C, Assets alpha, timeslots Monday 11:00
    def test_get_products_with_postalcode_1000_weekday_monday(self):

        # Get API response
        response = self.client.get(reverse('rest_api:products-list'),
                                   {'postalcode': '1000', 'weekdays': '1'})
        # Check that status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extract the json from the response
        response_data = response.json()
        # Check that the number of products is correct
        self.assertEqual(len(response_data), 2)

        # Check that the first stream is correct
        self.assertEqual(response_data[0]['stream_name'], 'Stream A')
        # Check that the first stream has 1 timeslot
        self.assertEqual(len(response_data[0]['availability']), 1)
        # Check that the first stream has 2 assets
        self.assertEqual(len(response_data[0]['assets']), 2)

        # Check that the second stream is correct
        self.assertEqual(response_data[1]['stream_name'], 'Stream C')
        # Check that the second stream has 1 timeslot
        self.assertEqual(len(response_data[1]['availability']), 1)
        # Check that the second stream has 1 asset
        self.assertEqual(len(response_data[1]['assets']), 1)
