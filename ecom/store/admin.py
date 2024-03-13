from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

# Mistura informações de profile e user


class ProfoleInline(admin.StackedInline):
    model = Profile

# Extende User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password']
    inlines = [ProfoleInline]


#
admin.site.unregister(User)

#
admin.site.register(User, UserAdmin)
