from django.db import models


class CostDetail(models.Model):
    cid = models.AutoField(db_column='cID', primary_key=True)  # Field name made lowercase.
    uid = models.IntegerField(db_column='uID')  # Field name made lowercase.
    ResName = models.CharField(db_column='ResName', max_length=20)  # Field name made lowercase.
    date = models.DateField()
    which_meal = models.IntegerField()
    rid = models.IntegerField(db_column='rID')  # Field name made lowercase.
    price = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    my_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '1_cost_detail'