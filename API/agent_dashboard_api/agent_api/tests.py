from django.test import TestCase
from .models import YourModel

class YourModelTestCase(TestCase):
    def setUp(self):
        # Set up initial data for the tests
        YourModel.objects.create(name='Example', age=30)

    def test_your_model(self):
        # Test case for your model's behavior
        obj = YourModel.objects.get(name='Example')
        self.assertEqual(obj.age, 30)
