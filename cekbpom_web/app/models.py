from django.db import models


class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    registration_no = models.CharField(max_length=512, blank=True)
    type = models.CharField(max_length=512, blank=True)
    name = models.CharField(max_length=512, blank=True)
    brand = models.CharField(max_length=512, blank=True)
    registrant = models.CharField(max_length=512, blank=True)
    producer = models.CharField(max_length=512, blank=True)
    validity = models.CharField(max_length=512, blank=True)
    location = models.CharField(max_length=512, blank=True)

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        return self.registration_no