from django.db import models
from django.core.validators import MinValueValidator
from .customer import Customer
from .giftCard import GiftCard

class Payment(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="donations")
    giftcard = models.OneToOneField(GiftCard, on_delete=models.DO_NOTHING,)
    payment_date = models.DateField(default="0000-00-00",)
    amount_donated = models.FloatField(validators=[MinValueValidator(0.00)], default = "0.00")
    description = models.CharField(max_length=200, default="I donated!", blank=True, null=False)

    class Meta:
        verbose_name = ("payment")
        verbose_name_plural = ("payments")
