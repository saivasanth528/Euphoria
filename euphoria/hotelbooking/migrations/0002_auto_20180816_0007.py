# Generated by Django 2.0.5 on 2018-08-15 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelbooking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel_users',
            name='isHotel_representative',
            field=models.BooleanField(default=True),
        ),
    ]