from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import FeedbackMessage, GalleryImage, Page


class StyledFormMixin:
    def _style_fields(self):
        for field in self.fields.values():
            css = 'input'
            if isinstance(field.widget, forms.Textarea):
                css = 'textarea'
            elif isinstance(field.widget, forms.CheckboxInput):
                css = 'checkbox'
            elif isinstance(field.widget, forms.Select):
                css = 'select'
            field.widget.attrs.setdefault('class', css)


class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self._style_fields()


class RegisterForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Повтор пароля'
        self._style_fields()


class PageForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'subtitle', 'content', 'show_in_menu')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Например: Прайс'}),
            'subtitle': forms.TextInput(attrs={'placeholder': 'Коротко, о чём страница'}),
            'content': forms.Textarea(attrs={'rows': 12, 'placeholder': 'Текст страницы'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Название'
        self.fields['subtitle'].label = 'Подзаголовок'
        self.fields['content'].label = 'Текст'
        self.fields['show_in_menu'].label = 'Показать в меню'
        self._style_fields()


class FeedbackForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = FeedbackMessage
        fields = ('name', 'email', 'phone', 'message')
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Расскажите, чем можем помочь'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class GalleryImageForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ('image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = 'Фотография'
        self.fields['image'].required = True
        self.fields['image'].widget.attrs['accept'] = 'image/*'
        self._style_fields()
