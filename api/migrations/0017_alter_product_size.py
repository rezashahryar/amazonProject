# Generated by Django 4.2.7 on 2024-03-03 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_size_product_available_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]