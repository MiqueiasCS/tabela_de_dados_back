from django.db import models

class Vunerabilities(models.Model):
    hostname = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(protocol='IPv4')
    title = models.CharField(max_length=255)
    severity = models.CharField(max_length=10)
    cvss = models.FloatField(null=True)
    publication_date = models.DateField(null=True)
    fixed = models.BooleanField(default=False)