from django.contrib import admin

from .models import Code, Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff']
    list_filter = []

    class Meta():
        model = User


# admin.site.register(Code)
admin.site.register(Follow)
