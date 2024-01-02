# Generated by Django 4.2.3 on 2023-08-04 00:33

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_image_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='JPEG', keep_meta=True, quality=75, scale=0.5, size=[500, 500], upload_to='post_images/'),
        ),
    ]
