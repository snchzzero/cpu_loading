# Generated by Django 4.0.5 on 2022-06-23 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelStartStop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Start_Model', models.CharField(default='Start', max_length=30)),
                ('Stop_Model', models.CharField(default='Stop', max_length=30)),
            ],
        ),
    ]