# Generated by Django 4.1 on 2022-09-27 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_product_views_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available_weight',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=6, verbose_name='доступный вес в кг'),
            preserve_default=False,
        ),
    ]