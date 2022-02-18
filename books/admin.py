from unicodedata import category
from django.contrib import admin

from .models import Category, Book
from .forms import BookForm

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'image_url')
    form = BookForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)

