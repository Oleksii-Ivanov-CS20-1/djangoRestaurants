# Generated by Django 5.1.4 on 2024-12-15 00:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0002_record'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='content',
        ),
        migrations.RemoveField(
            model_name='record',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='record',
            name='title',
        ),
        migrations.RemoveField(
            model_name='record',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='record',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cafes.category', verbose_name='category'),
        ),
        migrations.AddField(
            model_name='record',
            name='description',
            field=models.TextField(default='No description available', verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='record',
            name='mainPhoto',
            field=models.ImageField(default='No description available', upload_to='restaurant_main_photo/', verbose_name='Photo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='name',
            field=models.CharField(default='No description available', max_length=150, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='phone',
            field=models.CharField(default='+38', max_length=13, verbose_name='Phone Number'),
        ),
        migrations.AddField(
            model_name='record',
            name='street',
            field=models.CharField(default='', max_length=200, verbose_name='Street'),
        ),
        migrations.AddField(
            model_name='record',
            name='types',
            field=models.ManyToManyField(to='cafes.types', verbose_name='types'),
        ),
        migrations.AddField(
            model_name='record',
            name='url',
            field=models.SlugField(default='No description available', max_length=160, unique=True),
            preserve_default=False,
        ),
    ]
