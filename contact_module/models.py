from django.db import models


# name in admin page ===> soheilimani
# password in admin page ===> 1382


class ContactUs(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')
    email = models.EmailField(max_length=200, verbose_name='ایمیل')
    full_name = models.CharField(max_length=150, verbose_name='نام و نام خانوادگی')
    message = models.TextField(verbose_name='متن پیام')
    is_read_by_admin = models.BooleanField(default=True, verbose_name='خوانده شده توسط ادمین')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد پیام')
    response = models.TextField(verbose_name='پاسخ ادمین', null=True, blank=True)

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'

    def __str__(self):
        return self.full_name


class CreateProfile(models.Model):
    image = models.ImageField(upload_to='profile')
