from django import template
import collections

register = template.Library()


@register.filter(name='sort')
def sort_dictValue(value):
    if isinstance(value,dict):
        new_dict = collections.OrderedDict()
        key_list = sorted(value.keys())
        for key in key_list:
            new_dict[key] = value[key]
        return new_dict
    elif isinstance(value,list):
        return sorted(value)
    else:
        return value
    listsort.is_safe = True
