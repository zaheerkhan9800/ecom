# Generated by Django 3.0.6 on 2020-06-13 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='subject',
            new_name='phone',
        ),
    ]
