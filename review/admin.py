from django.contrib import admin

from .models import Review

@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_disply = '__all__'
