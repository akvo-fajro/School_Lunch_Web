from django.db import models

# Create your models here.

class Announcement(models.Model):
    announce = models.CharField(max_length=200)