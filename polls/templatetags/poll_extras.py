from django import template
from jalali_date import date2jalali

register = template.Library()


@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, "")


@register.filter(name='show_jalali_date')
def show_jalali_date(value):
    return date2jalali(value)


@register.filter(name='there_digits_currency')
def there_digits_currency(value: int):
    return '{:,}'.format(value)


@register.simple_tag()
def multiply(price, quality, *args, **kwargs):
    return there_digits_currency(quality * price)
