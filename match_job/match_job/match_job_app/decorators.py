
from django.db import models
from django.core.exceptions import ObjectDoesNotExist



from django.shortcuts import redirect


def checking_role(role: str):
    def checking_role(func):
        def wrapper(request,*args,**kwargs):
            user_group = request.user.groups.first().name
            if user_group != role:
                return redirect('home')
            else:
                result = func(request,*args,**kwargs)
                return result
        return wrapper
    return checking_role

            