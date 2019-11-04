from django.core.validators import MinValueValidator
from django.db import models
from .company import Company



class GiftCard(models.Model):

    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name="payments")
    barcode = models.CharField(max_length=20)
    initial_balance = models.FloatField(validators=[MinValueValidator(0.00)],)
    remaining_balance = models.FloatField(validators=[MinValueValidator(0.00)],)

    class Meta:
        verbose_name = ("giftcard")
        verbose_name_plural = ("giftcards")