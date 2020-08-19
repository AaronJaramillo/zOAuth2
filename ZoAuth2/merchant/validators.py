import re
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_address(value):
    #TODO validate checksum
    if settings.DEFAULT_CURRENCY == "rZEC":

        if not re.match(r'^zregtestsapling[a-zA-Z0-9]{76}$', value):
            raise ValidationError(
                '%(value)s z-address format is invalid',
                params={'value': value},
            )
