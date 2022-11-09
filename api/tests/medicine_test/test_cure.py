import pytest
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import CureFactory
from medicine.models import Cure

class CureGetTest(APITestCase):

        def test_class_get_list(self):
            CureFactory()
            CureFactory()
            raise Exception(Cure.objects.all()[0].date)
            response = self.client.get('/medicine/cure/')
            # raise Exception(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)


