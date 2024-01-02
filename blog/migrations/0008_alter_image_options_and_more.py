# Generated by Django 4.2.1 on 2023-07-18 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['created'], 'verbose_name': 'تصویر', 'verbose_name_plural': 'تصویر ها'},
        ),
        migrations.AddIndex(
            model_name='image',
            index=models.Index(fields=['created'], name='blog_image_created_1ba45b_idx'),
        ),
    ]