from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'image', 'model', 'color', 'fabrication', 'mileage', 'price', 'full_text', 'date']
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Марка авто'}),
            "model": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Модель авто'}),
            "image": forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            "color": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Цвет'}),
            "fabrication": forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Дата выпуска (ГГГГ-ММ-ДД)'}),
            "mileage": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Пробег, км'}),
            "price": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена, р'}),
            "full_text": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание'}),
            "date": forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Дата и время публикации'}),
        }








# from .models import Announcement
# from django.forms import ModelForm,TextInput, DateTimeInput, NumberInput,DateInput,Textarea,FileInput


# class AnnouncementForm(ModelForm):
#     class Meta:
#         model = Announcement
#         fields = ['title','image','model','color','fabrication', 'mileage','price','full_text','date']

#         widgets = {
#             "title": TextInput(attrs={
#                 'class':'form-control',
#                 'placeholder':'Марка авто'
#             }),
#             "model": TextInput(attrs={
#                 'class':'form-control',
#                 'placeholder':'Модель авто'
#             }),
#             "image": FileInput(attrs={
#                 'class':'form-control',
#                 'accept':'image/*'
#             }),
#             "color": TextInput(attrs={
#                 'class':'form-control',
#                 'placeholder':'Цвет'
#             }),
#             "fabrication": DateInput(attrs={
#                 'class':'form-control',
#                 'placeholder':'Дата выпуска'
#             }),
#             "mileage": NumberInput(attrs={
#                 'class':'form-control',
#                 'placeholder':'Пробег, км'
#             }),
#             "price": NumberInput(attrs={
#                 'class':'form-control',
#                 'placeholder':'Цена, р'
#             }),
#             "full_text": Textarea(attrs={
#                 'class':'form-control',
#                 'class':'textarea',
#                 'placeholder':'Описание'
#             }),
#             "date": DateTimeInput(attrs={
#                 'class':'form-control',
#                 'placeholder':'Дата и время публикации'
#             }),
            
#         }
