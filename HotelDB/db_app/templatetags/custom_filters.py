from django import template

register = template.Library()

@register.filter
def zip(a, b):
    return zip(a, b)

@register.filter
def multiply(value, arg):
    return float(value) * float(arg) 