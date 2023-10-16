from django.contrib import admin
from . import models


# Register your models here.


class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title']


class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'is_active']
    list_editable = ['is_active']


admin.site.register(models.SiteSetting)
admin.site.register(models.FooterLinkBox)
admin.site.register(models.FooterLink, FooterLinkAdmin)
admin.site.register(models.Slider, SliderAdmin)
admin.site.register(models.SiteBanner)
