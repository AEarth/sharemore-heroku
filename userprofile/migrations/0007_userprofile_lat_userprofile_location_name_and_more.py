# Generated by Django 4.2.5 on 2023-11-15 04:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "userprofile",
            "0006_alter_userprofile_full_text_alter_userprofile_image_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
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
            model_name="userprofile",
            name="location_name",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Location Name"
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
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