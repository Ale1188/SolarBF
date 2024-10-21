# Generated by Django 4.2.16 on 2024-10-21 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='address',
            new_name='street_address',
        ),
        migrations.AddField(
            model_name='customuser',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='zip_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
