# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Restaurant(models.Model):
    rid = models.IntegerField(db_column='rID', primary_key=True)  # Field name made lowercase.
    rname = models.TextField(db_column='rName')  # Field name made lowercase.
    rmap_score = models.CharField(db_column='rMap_Score', max_length=10)  # Field name made lowercase.
    rphone = models.TextField(db_column='rPhone')  # Field name made lowercase.
    raddress = models.TextField(db_column='rAddress')  # Field name made lowercase.
    sun = models.CharField(db_column='Sun', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mon = models.CharField(db_column='Mon', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tue = models.CharField(db_column='Tue', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wed = models.CharField(db_column='Wed', max_length=100, blank=True, null=True)  # Field name made lowercase.
    thur = models.CharField(db_column='Thur', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fri = models.CharField(db_column='Fri', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sat = models.CharField(db_column='Sat', max_length=100, blank=True, null=True)  # Field name made lowercase.
    all_label = models.CharField(max_length=100)
    meal_or_not = models.IntegerField()

    class Meta:
        managed = False
        db_table = '1_restaurant'
