from django.core.exceptions import ValidationError
from decimal import Decimal


class ImmutableFieldsMixin:
    immutable_fields = []
    error_message = None

    def save(self, *args, **kwargs):
        if self.pk:  # Only apply checks on existing instances
            instance=self.__class__.objects.get(pk=self.pk)
            for field in self.immutable_fields:
                if Decimal(instance.revenue) > Decimal('0.00'):
                    self.error_message = (
                        f"The field '{field}' is immutable and cannot be modified."
                    )
                    raise ValidationError(self.error_message)
        super().save(*args, **kwargs)
        return True
