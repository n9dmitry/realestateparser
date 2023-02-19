from django.db import models

# Create your models here.

class Source(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.title}"

class Advertisement(models.Model):
    date = models.DateTimeField()
    phone = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)
    title = models.CharField(max_length=300)
    price = models.IntegerField(blank=True, null=True)
    appartment_square = models.IntegerField()
    appartment_floor = models.IntegerField()
    floors_count = models.IntegerField()
    marketing_source = models.ForeignKey(Source, on_delete = models.CASCADE)