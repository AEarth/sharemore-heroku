# Generated by Django 4.2.5 on 2023-11-18 01:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0002_alter_lendrequest_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="lat",
            field=models.DecimalField(
                blank=True,
                decimal_places=6,
                max_digits=9,
                null=True,
                verbose_name="Latitude",
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="location_name",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Location Name"
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="lon",
            field=models.DecimalField(
                blank=True,
                decimal_places=6,
                max_digits=9,
                null=True,
                verbose_name="Longitude",
            ),
        ),
    ]
