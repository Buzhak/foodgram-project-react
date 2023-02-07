from django.contrib import admin

from .models import Code, User, Follow

admin.site.register(User)
admin.site.register(Code)
admin.site.register(Follow)
