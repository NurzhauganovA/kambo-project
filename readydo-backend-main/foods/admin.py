from django.contrib import admin
from foods.models import Food, Favorites, Estimation


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'grade', 'cuisine', 'taste')
    ordering = ('id',)


@admin.register(Favorites)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'food', 'user')
    ordering = ('id',)


@admin.register(Estimation)
class EstimationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'grade', 'type', 'value_id')
    ordering = ('id',)
