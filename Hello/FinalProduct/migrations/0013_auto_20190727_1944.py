# Generated by Django 2.2.3 on 2019-07-27 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FinalProduct', '0012_customer_purchase_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_order',
            name='Progress',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email_id',
            field=models.CharField(default='customer@gmail.com', max_length=60),
        ),
        migrations.AlterField(
            model_name='purchase_order',
            name='name',
            field=models.CharField(default='PO', max_length=50),
        ),
    ]
