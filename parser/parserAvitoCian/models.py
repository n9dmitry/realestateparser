from django.db import models

# Create your models here.

class Source(models.Model):
    title = models.CharField(max_length=50)

class Advertisement(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=300)
    appartment_square = models.IntegerField()
    appartment_floor = models.IntegerField()
    floors_count = models.IntegerField()
    marketing_source = models.ForeignKey(Source, on_delete = models.CASCADE)