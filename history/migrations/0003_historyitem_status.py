# Generated by Django 4.1.1 on 2022-09-19 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_remove_historyitem_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyitem',
            name='status',
            field=models.CharField(default='', max_length=20),
        ),
    ]
