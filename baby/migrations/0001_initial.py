# Generated by Django 4.2.2 on 2023-09-30 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserBaby',
            fields=[
                ('buyid', models.AutoField(db_column='buyID', primary_key=True, serialize=False)),
                ('uid', models.IntegerField(db_column='uID')),
                ('babyid', models.IntegerField(db_column='babyID')),
            ],
            options={
                'db_table': '1_user_baby',
                'managed': False,
            },
        ),
    ]
