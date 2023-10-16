from django.db import models

from account_module.models import User
from jalali_date import date2jalali, datetime2jalali


# Create your models here.


class ArticleCategory(models.Model):
    parent = models.ForeignKey('ArticleCategory', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='دسته بندی والد')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url_title = models.CharField(max_length=100, unique=True, verbose_name='عنوان لینک')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقالات'


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, db_index=True, allow_unicode=True, verbose_name='لینک')
    image = models.ImageField(upload_to='article', verbose_name='تصویر مقاله')
    text = models.TextField(verbose_name='توضیحات')
    selected_category = models.ManyToManyField(ArticleCategory, verbose_name='دسته بندی مقالات')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    auther = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=False, verbose_name='نویسنده')
    create_date = models.DateTimeField(auto_now_add=True, editable=False, null=True, verbose_name='تاریخ ثبت')
    tag = models.CharField(max_length=120, null=True, blank=True, verbose_name='برچسب مقاله')

    def __str__(self):
        return self.title

    def get_jalali_create_date(self):
        return date2jalali(self.create_date)

    def get_jalali_create_time(self):
        return self.create_date.strftime('%H : %M')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


class ArticleCommends(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مقاله')
    parent = models.ForeignKey('ArticleCommends', on_delete=models.CASCADE, blank=True, null=True, verbose_name='والد')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    create_deta = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='متن پیام')

    class Meta:
        verbose_name = 'نظر مقاله'
        verbose_name_plural = 'نظرات مقالات'

    def __str__(self):
        return str(self.user)