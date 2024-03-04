# Generated by Django 4.2.7 on 2024-03-03 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_product_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_sizes', to='api.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='available_size',
            field=models.ManyToManyField(blank=True, related_name='sizes_of_product', to='api.size'),
        ),
    ]