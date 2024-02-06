from .models import *


def decorator_base(func):
    def _decorator(request, *args, **kwargs):
        categories = Category.objects.all()

        context_dict= {
            "categories": categories,

        }

        return func(request, context_dict, *args, **kwargs)

    return _decorator