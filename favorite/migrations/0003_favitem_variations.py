# Generated by Django 3.1 on 2023-03-01 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation'),
        ('favorite', '0002_auto_20230228_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='favitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.Variation'),
        ),
    ]
