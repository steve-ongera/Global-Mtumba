# Generated by Django 4.2.5 on 2023-10-07 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_alter_cartdetail_quantity_alter_order_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_coupon', to='orders.coupon'),
        ),
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(default='PKIAZO33', max_length=20),
        ),
    ]