# Generated by Django 4.0.5 on 2022-06-27 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpu_ldng', '0007_modelstartstop_create_fig_model_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modelstartstop',
            old_name='Update_Model',
            new_name='Reset_Model',
        ),
    ]
