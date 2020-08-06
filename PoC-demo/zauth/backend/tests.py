from django.test import TestCase
import datetime
from .models import Transaction, Product
from api.models import OAuth2Client

# Create your tests here.

class TransactionModelTests(TestCase):

    def setUp(self):

        self.product = Product(
            name='Product1',
            address='zaddr1234',
            period=datetime.timedelta(86000),
            scope='product1',
            price=100000000
            )
        self.transaction = Transaction(
            txid='1234567876543',
            address='zaddr1234',
            amount=100000000, memo='2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d466b77457759484b6f5a497a6a3043415159494b6f5a497a6a304441516344516741457130594c6a355470704851706c45583352615a6f4e334569693969680a506f635a616b62556e7555365a73776e55694f47487366524e613934324d476b79484b5532566d564d4f78666e517064527163676b6c336371773d3d0a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a'
        )
        self.transaction.save()
        self.product.save()

    def test_process_transaction(self):
        print(self.product.price)

        self.transaction.process_transaction()
        self.assertEquals(self.transaction.processed, True)
        self.assertEquals(self.transaction.invalid, False)

    def test_client_created_after_tx(self):
        self.transaction.process_transaction()
        client = OAuth2Client.objects.get(public_key=bytes.fromhex(self.transaction.memo))
        self.assertEquals(client.scope, 'product1')
