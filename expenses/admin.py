from django.contrib import admin
from .models import  Expense, Balance
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin

admin.site.register(Expense)
admin.site.register(Balance)

# class CustomUInline(admin.StackedInline):
#     model = CustomUser
#     can_delete = False
#     verbose_name_plural = 'CustomUsers'

# class CustomizedUA(UserAdmin):
#     inlines = (CustomUInline,)

# admin.site.unregister(User)
# admin.site.register(User, CustomizedUA)


