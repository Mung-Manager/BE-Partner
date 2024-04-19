from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class PhoneNumberValidator(RegexValidator):
    regex = r"^010-\d{4}-\d{4}$"
    message = "Enter a valid phone number (e.g. 010-0000-0000)."

    def __call__(self, value):
        try:
            super().__call__(value)
        except ValidationError:
            raise ValidationError(self.message, code=self.code)
