from django import forms
from django.core.exceptions import ValidationError

from .models import Book

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('title', 'isbn', 'category',)

    def clean_isbn(self):
        import re
        isbn_data = self.cleaned_data['isbn']
        m = re.match(r'^\d{13}$', isbn_data)
        if not m:
            raise ValidationError('13桁の数字のみを入力してください')
        return isbn_data
