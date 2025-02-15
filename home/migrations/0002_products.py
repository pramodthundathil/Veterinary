# Generated by Django 5.0.6 on 2025-01-09 16:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('pet', models.CharField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('fish', 'Fish'), ('reptile', 'Reptile'), ('small_pet', 'Small Pet'), ('other', 'Other')], max_length=100)),
                ('category', models.CharField(choices=[('food', 'Food'), ('toys', 'Toys'), ('accessories', 'Accessories'), ('grooming', 'Grooming'), ('health', 'Health'), ('habitat', 'Habitat')], max_length=200)),
                ('image', models.FileField(upload_to='product_image')),
                ('price', models.FloatField()),
                ('stock', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
