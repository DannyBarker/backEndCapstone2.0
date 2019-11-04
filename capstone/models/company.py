from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):

    name = models.CharField(max_length=55)


    class Meta:
        verbose_name = ("company")
        verbose_name_plural = ("companies")
