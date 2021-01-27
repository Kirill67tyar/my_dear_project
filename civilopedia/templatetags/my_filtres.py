from django import template

register = template.Library()


@register.filter(name='get_int')
def get_int(value):
    return int(value)

@register.filter(name='get_negative')
def get_negative(value):
    return -value


@register.filter(name='get_float')
def get_float(value):
    return 5 - 1.5

@register.filter(name='subtract')
def subtract(value, subtrahend):
    return value - subtrahend