from django.db import models

class NetworkGPS(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    gps = models.CharField(max_length=250, null=False, blank=False)

    def __str__(self):
       return self.name

    class Meta:
        managed = True
        db_table = 'network_gps'


class Attendances(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    employee_id =  models.CharField(max_length=25, null=False, blank=False)
    tg_id = models.CharField(max_length=25, null=True,blank=True)
    phone = models.CharField(max_length=25, null=False, blank=False)
    branch =  models.CharField(max_length=50, null=False, blank=False)
    gps_in= models.CharField(max_length=250, null=True, blank=True)
    address_in= models.CharField(max_length=250, null=True, blank=True)
    date_in= models.DateTimeField(null=True, blank=True)
    clock_in = models.CharField(max_length=50, null=True, blank=True)
    gps_out =models.CharField(max_length=250, null=True, blank=True)
    address_out= models.CharField(max_length=250, null=True, blank=True)
    date_out= models.DateTimeField( null=True, blank=True)
    clock_out=models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
       return self.name

    class Meta:
        managed = True
        db_table = 'attendances'