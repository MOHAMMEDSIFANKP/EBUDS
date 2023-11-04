# Generated by Django 4.2.6 on 2023-10-31 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0051_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Return', 'Return'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Processing', 'Processing'), ('Cancelled', 'Cancelled')], default='Pending', max_length=150),
        ),
    ]
