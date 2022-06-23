from django.db import models

class ModelStartStop(models.Model):
    Start_Model = models.CharField(max_length=30, default="novalue", blank=True)
    Stop_Model = models.CharField(max_length=30, default="novalue", blank=True)
