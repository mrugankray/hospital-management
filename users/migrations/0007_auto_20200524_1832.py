# Generated by Django 3.0.5 on 2020-05-24 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_prescription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prescription',
            old_name='patient_name',
            new_name='patient_fullname',
        ),
        migrations.AddField(
            model_name='prescription',
            name='patient_username',
            field=models.CharField(default='default', max_length=50),
        ),
    ]
