import string

from django import forms

from catalog.models import Product


class ProductForm(forms.ModelForm):
    """Класс для валидации формы создания и изменения продукта"""

    words_blacklist = {'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар'}

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'preview']

    def is_word_in_blacklist(self, word: str) -> bool:
        return word.lower() in self.words_blacklist

    @staticmethod
    def remove_punctuation(text: str) -> str:
        return text.translate(str.maketrans('', '', string.punctuation))

    def has_word_in_blacklist(self, text: str) -> bool:
        clean_text = self.remove_punctuation(text)
        words = clean_text.split()
        result = any(map(self.is_word_in_blacklist, words))
        return result

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        if self.has_word_in_blacklist(cleaned_data):
            raise forms.ValidationError('Текст содержит запрещенное слово')
        return cleaned_data
