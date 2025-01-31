# Generated by Django 5.1.5 on 2025-01-31 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='img_url',
            field=models.ImageField(null=True, upload_to='posts/images'),
        ),
    ]
