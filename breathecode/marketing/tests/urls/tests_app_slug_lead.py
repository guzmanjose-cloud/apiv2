"""
Test /academy/app_slug_lead
"""
from django.utils import timezone
from datetime import timedelta
import re, string
from random import choice, choices, randint
from mixer.main import Mixer
from unittest.mock import MagicMock, patch
from django.urls.base import reverse_lazy
from rest_framework import status
from faker import Faker
from breathecode.tests.mocks import (
    GOOGLE_CLOUD_PATH,
    apply_google_cloud_client_mock,
    apply_google_cloud_bucket_mock,
    apply_google_cloud_blob_mock,
)
from ..mixins import MarketingTestCase

fake = Faker()


class AppSlugLeadTestSuite(MarketingTestCase):
    """Test /academy/app_slug_lead"""
    @patch('breathecode.marketing.tasks.persist_single_lead', MagicMock())
    def test_app_slug_lead__without_app_slug_or_app_id(self):
        from breathecode.marketing.tasks import persist_single_lead

        url = reverse_lazy('marketing:app_slug_lead', kwargs={'app_slug': 'they-killed-kenny'})
        response = self.client.post(url)

        json = response.json()
        expected = {'detail': 'without-app-slug-or-app-id', 'status_code': 400}

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.all_lead_generation_app_dict(), [])

        self.assertEqual(persist_single_lead.call_args_list, [])

    @patch('breathecode.marketing.tasks.persist_single_lead', MagicMock())
    def test_app_slug_lead__without_app_id(self):
        from breathecode.marketing.tasks import persist_single_lead
        model = self.generate_models(lead_generation_app=True)

        url = (reverse_lazy('marketing:app_slug_lead', kwargs={'app_slug': 'they-killed-kenny'}) +
               f'?app_id={model.lead_generation_app.app_id}')
        response = self.client.post(url)

        json = response.json()
        expected = {'detail': 'without-app-id', 'status_code': 401}

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.all_lead_generation_app_dict(),
                         [self.model_to_dict(model, 'lead_generation_app')])

        self.assertEqual(persist_single_lead.call_args_list, [])

    @patch('breathecode.marketing.tasks.persist_single_lead', MagicMock())
    def test_app_slug_lead__without_required_fields(self):
        from breathecode.marketing.tasks import persist_single_lead
        model = self.generate_models(lead_generation_app=True)

        url = (reverse_lazy('marketing:app_slug_lead', kwargs={'app_slug': model.lead_generation_app.slug}) +
               f'?app_id={model.lead_generation_app.app_id}')

        start = timezone.now()
        response = self.client.post(url)
        end = timezone.now()

        json = response.json()
        expected = {'language': ['This field may not be null.']}

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        db = self.all_lead_generation_app_dict()
        last_call_at = db[0]['last_call_at']

        self.assertGreater(end, last_call_at)
        self.assertGreater(last_call_at, start)

        db[0]['last_call_at'] = None

        self.assertEqual(db, [{
            **self.model_to_dict(model, 'lead_generation_app'),
            'hits': 1,
            'last_call_status': 'ERROR',
            'last_request_data': '{}',
        }])

        self.assertEqual(persist_single_lead.call_args_list, [])

    @patch('breathecode.marketing.tasks.persist_single_lead', MagicMock())
    def test_app_slug_lead__without_required_fields__(self):
        from breathecode.marketing.tasks import persist_single_lead

        model = self.generate_models(lead_generation_app=True)

        url = (reverse_lazy('marketing:app_slug_lead', kwargs={'app_slug': model.lead_generation_app.slug}) +
               f'?app_id={model.lead_generation_app.app_id}')
        data = {'language': 'eo'}

        start = timezone.now()
        response = self.client.post(url, data, format='json')
        end = timezone.now()

        json = response.json()

        created_at = self.iso_to_datetime(json['created_at'])
        updated_at = self.iso_to_datetime(json['updated_at'])

        self.assertGreater(end, created_at)
        self.assertGreater(created_at, start)

        self.assertGreater(end, updated_at)
        self.assertGreater(updated_at, start)

        del json['created_at']
        del json['updated_at']

        expected = {
            'ac_contact_id': None,
            'ac_deal_id': None,
            'ac_expected_cohort': None,
            'academy': 1,
            'automation_objects': [],
            'automations': '',
            'browser_lang': None,
            'city': None,
            'client_comments': None,
            'contact': None,
            'country': None,
            'course': None,
            'current_download': None,
            'deal_status': None,
            'email': None,
            'fb_ad_id': None,
            'fb_adgroup_id': None,
            'fb_form_id': None,
            'fb_leadgen_id': None,
            'fb_page_id': None,
            'first_name': '',
            'gclid': None,
            'id': 1,
            'language': 'eo',
            'last_name': '',
            'latitude': None,
            'lead_generation_app': 1,
            'lead_type': None,
            'location': None,
            'longitude': None,
            'phone': None,
            'referral_key': None,
            'sentiment': None,
            'state': None,
            'storage_status': 'PENDING',
            'street_address': None,
            'tag_objects': [],
            'tags': '',
            'user': None,
            'utm_campaign': None,
            'utm_medium': None,
            'utm_source': None,
            'utm_url': None,
            'won_at': None,
            'zip_code': None,
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(self.all_form_entry_dict(), [{
            'ac_contact_id': None,
            'ac_deal_id': None,
            'ac_expected_cohort': None,
            'academy_id': 1,
            'automations': '',
            'browser_lang': None,
            'city': None,
            'client_comments': None,
            'contact_id': None,
            'country': None,
            'course': None,
            'current_download': None,
            'deal_status': None,
            'email': None,
            'fb_ad_id': None,
            'fb_adgroup_id': None,
            'fb_form_id': None,
            'fb_leadgen_id': None,
            'fb_page_id': None,
            'first_name': '',
            'gclid': None,
            'id': 1,
            'language': 'eo',
            'last_name': '',
            'latitude': None,
            'lead_generation_app_id': 1,
            'lead_type': None,
            'location': None,
            'longitude': None,
            'phone': None,
            'referral_key': None,
            'sentiment': None,
            'state': None,
            'storage_status': 'PENDING',
            'street_address': None,
            'tags': '',
            'user_id': None,
            'utm_campaign': None,
            'utm_medium': None,
            'utm_source': None,
            'utm_url': None,
            'won_at': None,
            'zip_code': None,
        }])

        db = self.all_lead_generation_app_dict()
        last_call_at = db[0]['last_call_at']

        self.assertGreater(end, last_call_at)
        self.assertGreater(last_call_at, start)

        db[0]['last_call_at'] = None

        self.assertEqual(db, [{
            **self.model_to_dict(model, 'lead_generation_app'),
            'hits': 1,
            'last_call_status': 'OK',
            'last_request_data': '{"language": "eo"}',
        }])

        self.assertEqual(persist_single_lead.call_args_list, [])