# Generated by Django 4.2.3 on 2023-09-03 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0012_alter_image_image_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ تولد ')),
                ('bio', models.TextField(blank=True, null=True, verbose_name=' بیوگرافی ')),
                ('photo', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, null=True, quality=60, scale=0.5, size=[500, 500], upload_to='profile_image/')),
                ('job', models.CharField(blank=True, max_length=120, null=True, verbose_name=' شغل ')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL, verbose_name='')),
            ],
            options={
                'verbose_name': 'اکانت',
                'verbose_name_plural': 'اکانت ها ',
            },
        ),
    ]
