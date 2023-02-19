from django.db import models

# Create your models here.

class Source(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.title}"

class Advertisement(models.Model):
    date = models.DateTimeField()
    phone = models.CharField(blank=True, null=True, max_length=50)
    url = models.CharField(max_length=1000, blank=True, null=True)
    title = models.CharField(max_length=300)
    price = models.IntegerField(blank=True, null=True)
    appartment_square = models.FloatField()
    appartment_floor = models.IntegerField()
    floors_count = models.IntegerField()
    marketing_source = models.ForeignKey(Source, on_delete = models.CASCADE)