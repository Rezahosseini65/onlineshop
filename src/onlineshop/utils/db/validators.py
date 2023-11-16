from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class PhoneNumberValidator(RegexValidator):
    regex = '^98(9[0-3,9]\d{8}|[1-9]\d{9})$'
    message = _('Phone number must be a VALID 12 digits like 98xxxxxxxxxx')
    code = _('Invalid Phone Number')

phone_nuber_validator = PhoneNumberValidator()