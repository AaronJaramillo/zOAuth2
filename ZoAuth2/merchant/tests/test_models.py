from django.test import TestCase
from merchant.models import Currency

class TestCurrencyModel(TestCase):
    def setUp(self):
        self.currency = Currency(ticker='rZEC')
        self.currency.save()

    def test_z_address_validation(self):
        zaddr = "zregtestsapling1rwzrm6cygnhkdqvp4kwwx0wuw8zf27j8elzgruvzzy567ye596fnyxrcnsff2vsy4m5jyl908eu"
        is_valid = self.currency.validate_address(zaddr)

        self.assertTrue(is_valid)
