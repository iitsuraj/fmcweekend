# Generated by Django 2.1 on 2018-09-19 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20180918_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='accomodation',
            field=models.IntegerField(default=0),
        ),
    ]