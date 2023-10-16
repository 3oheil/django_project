from django.db import models


# Create your models here.

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, verbose_name='نام سایت')
    site_url = models.CharField(max_length=100, verbose_name='دامنه سایت')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='تلفن')
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name='آدرس')
    email = models.CharField(max_length=25, verbose_name='ایمیل')
    fax = models.CharField(max_length=18, null=True, blank=True, verbose_name='فکس')
    logo = models.ImageField(upload_to='images/sire_setting/', verbose_name='تصویر لوگو')
    copy_right = models.TextField(verbose_name='متن کپی رایت')
    about_us = models.TextField(verbose_name='درباره ما')
    is_mean_site = models.BooleanField(default=False, verbose_name='تنظیمات اضلی')

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته یندی لینک های فوتر'
        verbose_name_plural = 'لینک های فوتر'


class FooterLink(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url_title = models.CharField(max_length=100, verbose_name='لینک')
    footer_link_box = models.ForeignKey(FooterLinkBox, on_delete=models.CASCADE, verbose_name='دسته بندی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'


class Slider(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    link_title = models.CharField(max_length=100, verbose_name='عنوان لینک')
    link = models.URLField(max_length=100, verbose_name='لینک')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to='images/slider', verbose_name='تصویر  اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'تنظیمات اسلایدر'


class SiteBanner(models.Model):
    class PositionBannerChoices(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات',
        product_detail = 'product_detail', 'صفحه توضیحات محصولات',
        about_us = 'about_us', 'درباره ما',
        contact_us = 'contact_us', 'تماس با ما'

    title = models.CharField(max_length=100, verbose_name='عنوان')
    url = models.URLField(max_length=300, null=True, blank=True, verbose_name='لینک')
    image = models.ImageField(upload_to='images/banner', verbose_name='تصویر بنر')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    position = models.CharField(max_length=250, choices=PositionBannerChoices.choices, verbose_name='جایگاه نمایش')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر تبلیغات'
        verbose_name_plural = 'بنر های تبلیغاتی'
