import re
from django import forms
from django.core.exceptions import ValidationError

from books.models import Book
from .models import Review, Comment


class ReviewModelForm(forms.ModelForm):
    isbn = forms.CharField(max_length=13)

    class Meta:
        model = Review
        fields = ('title', 'body', 'status', 'recommending_text',)

    def clean_isbn(self):
        isbn_cleaned_data = self.cleaned_data['isbn']
        m = re.match(r'^\d{13}$', isbn_cleaned_data)
        if not m:
            raise ValidationError('13桁の数字のみを入力してください。')
        try:
            Book.objects.get(isbn=isbn_cleaned_data)
            return isbn_cleaned_data
        except Book.DoesNotExist:
            raise ValidationError('該当する本が当サイトに登録されていません。ページ上部のナビゲーションバーから本を登録してください。')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)