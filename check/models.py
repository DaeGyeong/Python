# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models


class NaverApiStatus(models.Model):
    api_seq = models.AutoField(primary_key=True)
    api_name = models.CharField(max_length=70, blank=True, null=True)
    api_type = models.CharField(max_length=20, blank=True, null=True)
    api_status = models.IntegerField(blank=True, null=True)
    api_time = models.DateTimeField(blank=True, null=True)

    class Meta:
#        managed = False
        db_table = 'naver_api_status'


class NaverApiErrorLog(models.Model):
    api_seq = models.AutoField(primary_key=True)
    api_name = models.CharField(max_length=70, blank=True, null=True)
    api_error_code = models.CharField(max_length=50, blank=True, null=True)
    api_error_time = models.DateTimeField(blank=True, null=True)

    class Meta:
#        managed = False
        db_table = 'naver_api_error_log'
