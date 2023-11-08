import string
from typing import Callable

from django import forms
from rapidfuzz import fuzz

from catalog.models import Product


class BackListMixin:
    words_blacklist = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар')
    blacklist_ratio_level = 80

    def is_similar_words(self, word_1: str) -> Callable:
        def check_ratio(word_2: str) -> bool:
            return fuzz.ratio(word_1, word_2) >= self.blacklist_ratio_level

        return check_ratio

    def is_word_in_blacklist(self, word: str) -> bool:
        return any(map(self.is_similar_words(word), self.words_blacklist))

    @staticmethod
    def remove_punctuation(text: str) -> str:
        return text.translate(str.maketrans('', '', string.punctuation))

    def has_word_in_blacklist(self, text: str) -> bool:
        clean_text = self.remove_punctuation(text)
        words = clean_text.split()
        result = any(map(self.is_word_in_blacklist, words))
        return result


class ProductForm(BackListMixin, forms.ModelForm):
    """Класс для валидации формы создания и изменения продукта"""

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'preview']

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        if self.has_word_in_blacklist(cleaned_data):
            raise forms.ValidationError('Текст содержит запрещенное слово')
        return cleaned_data
