# Generated by Django 2.2.3 on 2019-07-19 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FinalProduct', '0010_components_process_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='components',
            name='Progress',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='finalproduct',
            name='Progress',
            field=models.IntegerField(default=0),
        ),
    ]