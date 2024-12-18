from django.contrib import admin
from forums.models import Forum, Message


@admin.register(Forum)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'grade')
    ordering = ('id',)


@admin.register(Message)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'forum', 'auther', 'message')
    ordering = ('id',)
