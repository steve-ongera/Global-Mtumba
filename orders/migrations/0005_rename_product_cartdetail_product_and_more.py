# Generated by Django 4.2.5 on 2023-10-06 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_cartdetail_quantity_alter_order_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartdetail',
            old_name='Product',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='total_After_coupon',
            new_name='total_after_coupon',
        ),
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(default='8ZBU93CD', max_length=20),
        ),
    ]
