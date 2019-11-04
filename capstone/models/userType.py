from django.db import models


class UserType(models.Model):

    type = models.CharField(max_length=55)


    class Meta:
        verbose_name = ("usertype")
        verbose_name_plural = ("usertypes")