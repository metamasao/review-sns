from django import forms
from django.core.exceptions import ValidationError

from .models import Book

class BookForm(forms.ModelForm):
    """
    本を登録する時に使用するformクラスです。
    正規表現を使って検証しています。
    """
    class Meta:
        model = Book
        fields = ('title', 'isbn', 'category',)

    def clean_isbn(self):
        """
        isbnフィールドに入力された値が数字のみでないまたは13字に満たない場合に
        バリエーションエラーを引き起こす。
        """
        import re
        isbn_data = self.cleaned_data['isbn']
        m = re.match(r'^\d{13}$', isbn_data)
        if not m:
            raise ValidationError('13桁の数字のみを入力してください。')
        return isbn_data
