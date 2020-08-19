import re
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.query import EmptyQuerySet
from authorization.models import OAuth2Client
from .validators import validate_address
# Create your models here.

class Currency(models.Model):
    ticker = models.CharField(max_length=4, default='ZEC', primary_key=True)
    last_block = models.PositiveIntegerField(blank=True, null=True, default=0)

    def update_last_block(self, blocknum):
        self.last_block = blocknum
        self.save()

        return self.last_block

    def validate_address(self, address):
        if self.ticker == 'rZEC':
            return re.match(r'^zregtestsapling[a-zA-Z0-9]{76}$', address)

class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=91, unique=True, validators=[validate_address])
    period = models.DurationField()
    scope = models.CharField(max_length=50)
    price = models.IntegerField(default=1)

class Transaction(models.Model):
    txid = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=91)
    amount = models.IntegerField()
    processed = models.BooleanField(default=False)
    invalid = models.BooleanField(default=False)
    ## Later add invoice status: Partially paid, double paid, invalid product etc
    memo = models.CharField(max_length=1024, null=True)

    def process_transaction(self):
        if self.processed:
            return self.processed
        product = Product.objects.filter(address=self.address).get()
        if isinstance(product, EmptyQuerySet):
            self.invalid = True
            self.processed = True
            self.save()
            return self.processed
        if self.amount >= product.price:
            ##Validate Memo Field Here
                ##ie: check is memo field contains a valid ECDSA public key
                ##    also check if public key already has a client object
            if OAuth2Client.objects.create_client_or_update_scope(
                    self.memo, product.scope):
                print('got to create_or_update')
                self.invalid = False
                self.processed = True
                self.save()
                return self.processed
        else:
            ##return processed = True, valid = False
            print('failed to create client')
            self.processed = True
            self.invalid = True
            self.save()
            return self.processed


