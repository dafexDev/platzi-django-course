from django.template.library import Library


register = Library()


@register.filter
def get_item(dictionary, key):
    return dictionary[key]
