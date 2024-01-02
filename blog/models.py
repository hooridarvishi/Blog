from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
from django.template.defaultfilters import slugify
from django_resized import ResizedImageField


# Managers
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


#
# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'
    CATEGORY_CHOICES = (
        ("تکنولوژی", "تکنولوژی"),
        ("زبان برنامه نویسی", "زبان برنامه نویسی"),
        ("هوش مصنوغی", "هوش مصنوعی"),
        ("بلاکچین", "بلاکچین"),
        ("سایر", "سایر"))
    category = models.CharField(max_length=120, choices=CATEGORY_CHOICES, default="سایر")
    # relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts", verbose_name="نویسنده")
    # data fields
    title = models.CharField(max_length=250, verbose_name="عنوان")
    description = models.TextField(verbose_name="توضیحات")
    slug = models.SlugField(max_length=250, verbose_name="اسلاگ")
    # date
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    # choice fields
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name="وضعیت")
    reading_time = models.PositiveIntegerField(verbose_name="زمان مطالعه")

    # objects = models.Manager()
    objects = jmodels.jManager()
    published = PublishedManager()
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = "پست"
        verbose_name_plural = "پست ها"
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage, img.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)


class Ticket(models.Model):
    message = models.TextField(verbose_name="پیام")
    name = models.CharField(max_length=250, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=11, verbose_name="شماره تماس")
    subject = models.CharField(max_length=250, verbose_name="موضوع")

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="پست")
    name = models.CharField(max_length=250, verbose_name="نام")
    body = models.TextField(verbose_name="متن کامنت")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    active = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f"{self.name}: {self.post}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images", verbose_name="تصویر")
    title = models.CharField(max_length=250, verbose_name="عنوان", null=True, blank=True)
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    image_file = models.ImageField(upload_to="post_images/")

    # image_file=ResizedImageField(upload_to="post_images/" , size=[500,500] , quality=75 , crop=["middle","center"] )
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "تصویر"
        verbose_name_plural = "تصویر ها"

    def __str__(self):
        return self.title if self.title else "none"


class Account(models.Model):
    user = models.OneToOneField(User, related_name="account", verbose_name="", on_delete=models.CASCADE)
    date_of_birth = jmodels.jDateField(verbose_name="تاریخ تولد ", blank=True, null=True)
    bio = models.TextField(verbose_name=" بیوگرافی ", blank=True, null=True)
    photo = ResizedImageField(upload_to="profile_image/", size=[500, 500], crop=["middle", "center"], quality=60,
                              blank=True, null=True)
    job = models.CharField(max_length=120, verbose_name=" شغل ", blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "اکانت"
        verbose_name_plural = "اکانت ها "
