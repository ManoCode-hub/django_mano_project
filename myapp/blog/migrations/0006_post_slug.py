# Generated by Django 5.1.5 on 2025-01-28 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_delete_category_post_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='example slug', unique=True),
            preserve_default=False,
        ),
    ]
