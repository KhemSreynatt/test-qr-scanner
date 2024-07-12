from django.db import models

class NetworkIP(models):
    name = models.CharField(max_length=50, null=False, blank=False)

