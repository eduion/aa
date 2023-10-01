# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class UserBaby(models.Model):
    buyid = models.AutoField(db_column='buyID', primary_key=True)  # Field name made lowercase.
    uid = models.IntegerField(db_column='uID')  # Field name made lowercase.
    babyid = models.IntegerField(db_column='babyID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '1_user_baby'
