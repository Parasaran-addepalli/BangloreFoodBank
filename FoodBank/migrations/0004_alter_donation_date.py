# Generated by Django 4.0.5 on 2022-06-26 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodBank', '0003_corpinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
