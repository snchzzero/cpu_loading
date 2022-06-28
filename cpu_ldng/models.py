from django.db import models

class ModelStartStop(models.Model):
    Start_Model = models.CharField(max_length=30, default="novalue", blank=True)
    Stop_Model = models.CharField(max_length=30, default="novalue", blank=True)
    Reset_Model = models.CharField(max_length=30, default="novalue", blank=True)
    Create_Fig_Model = models.CharField(max_length=30, default="novalue", blank=True)
    Send_Fig_Model = models.CharField(max_length=30, default="novalue", blank=True)

