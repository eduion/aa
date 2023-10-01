# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Rlabel(models.Model):
    rid = models.AutoField(db_column='rID', primary_key=True)  # Field name made lowercase.
    all_label = models.CharField(max_length=100)
    label_1 = models.CharField(max_length=100)
    label_2 = models.CharField(max_length=100, blank=True, null=True)
    label_3 = models.CharField(max_length=100, blank=True, null=True)
    label_4 = models.CharField(max_length=100, blank=True, null=True)
    label_5 = models.CharField(max_length=100, blank=True, null=True)
    label_6 = models.CharField(max_length=100, blank=True, null=True)
    label_7 = models.CharField(max_length=100, blank=True, null=True)
    label_8 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '1_rlabel'
