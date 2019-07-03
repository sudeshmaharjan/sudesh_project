from django.db import models

class Employeer(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.BigIntegerField()


    def __str__(self):
        return self.first_name