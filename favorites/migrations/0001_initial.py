# Generated by Django 4.1.1 on 2022-09-14 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavoritesItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(max_length=18)),
                ('product_id', models.IntegerField(max_length=18)),
                ('count', models.IntegerField(max_length=6)),
            ],
        ),
    ]
