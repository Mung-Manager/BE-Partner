from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from mung_manager.common.constants import SYSTEM_CODE


class PhoneNumberValidator(RegexValidator):
    regex = r"^010-\d{4}-\d{4}$"
    message = SYSTEM_CODE.message("INVALID_PHONE_NUMBER")

    def __call__(self, value):
        try:
            super().__call__(value)
        except ValidationError:
            raise ValidationError(self.message, code=self.code)


class UniquePetNameValidator:
    message = SYSTEM_CODE.message("UNIQUE_PET_NAME")
    code = SYSTEM_CODE.code("UNIQUE_PET_NAME")

    def __call__(self, value):
        if len(value) != len(set(value)):
            raise ValidationError(message=self.message, code=self.code)
