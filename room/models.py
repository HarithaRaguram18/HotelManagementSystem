# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=255, default = '')
    room_type_id = models.CharField(max_length=255, default = "")
    room_bed_id = models.CharField(max_length=255, default = "")
    room_price = models.CharField(max_length=255, default = "")
    room_image = models.CharField(max_length=255, null = True)
    room_description = models.TextField(default = "")
    room_facility = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.room_name    
