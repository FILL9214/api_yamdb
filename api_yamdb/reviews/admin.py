from django.contrib import admin
from .models import Review, Comment, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
    )
    search_fields = ('username', 'email')
    list_filter = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Review)
admin.site.register(Comment)
