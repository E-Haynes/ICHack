from django.template.defaulttags import register
import datetime

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(expects_localtime=True)
def is_expiring_than_two_days(value):
    if isinstance(value, datetime.datetime):
        value = value.date()
    delta = value - datetime.date.today()
    return delta.days <= 2