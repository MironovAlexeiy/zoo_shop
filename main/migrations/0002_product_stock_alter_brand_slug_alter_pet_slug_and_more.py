# Generated by Django 4.1 on 2022-08-20 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=models.SlugField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='pet',
            name='slug',
            field=models.SlugField(max_length=250, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='slug',
            field=models.SlugField(max_length=250, unique=True),
        ),
    ]
