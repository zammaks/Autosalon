# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import Client

# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(max_length=128, required=True)
#     last_name = forms.CharField(max_length=128, required=True)
#     phone_number = forms.CharField(max_length=15, required=True)
#     birth_date = forms.DateField(required=False)
#     gender = forms.ChoiceField(choices=Client.GENDER_CHOICES, required=False)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'birth_date', 'gender')

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#             client = Client(
#                 user=user,
#                 first_name=self.cleaned_data['first_name'],
#                 last_name=self.cleaned_data['last_name'],
#                 phone_number=self.cleaned_data['phone_number'],
#                 birth_date=self.cleaned_data['birth_date'],
#                 gender=self.cleaned_data['gender']
#             )
#             client.save()
#         return user
    
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Client, Review
from .models import Service,Salon

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='',required=True, widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Электронная почта'}))
    first_name = forms.CharField(label='', max_length=128, required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Имя'}))
    last_name = forms.CharField(label='', max_length=128, required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Фамилия'}))
    second_name = forms.CharField(label='', max_length=128, required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Отчество'}))
    phone_number = forms.CharField(label='', max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Телефон'}))
    birth_date = forms.DateField(label='', required=False, widget=forms.DateInput(attrs={'class': 'form-control','placeholder': 'Дата рождения'}))
    gender = forms.ChoiceField(label='', choices=Client.GENDER_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control','placeholder': 'Пол'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'last_name','first_name', 'second_name', 'phone_number', 'birth_date', 'gender')

        widgets = { 
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Никнейм'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email*'}), 
            'password1': forms.PasswordInput(attrs={'class': 'password','id':'#password', 'placeholder': 'Пароль*'}), 
            'password2': forms.PasswordInput(attrs={'class': 'password', 'placeholder': 'Подтверждение пароля*'}), 
        }

        labels = {
            'username': '',
            'last_name': '',
            'first_name': '',
            'second_name': '',
            'email': '',
            'phone_number': '',
            'birth_date': '',
            'gender': '',
            'password1': '',
            'password2': '',
        }
        help_texts = {
            'password1': '',
            'password2': '',
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            client = Client(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                second_name=self.cleaned_data['second_name'],
                phone_number=self.cleaned_data['phone_number'],
                birth_date=self.cleaned_data['birth_date'],
                gender=self.cleaned_data['gender']
            )
            client.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Никнейм'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }




class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'execution_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Название услуги'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Описание услуги'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Стоимость, p'}),
            'execution_time': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Затраченное время (дней)', 'style':"height:50px;"}),
        }
        labels = {
            'name': '',
            'description': '',
            'price': '',
            'execution_time': ''}




class ServiceFilterForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False, label="Выберите клиента")
    min_price = forms.DecimalField(min_value=0, required=False, label="Минимальная цена", widget=forms.NumberInput(attrs={'step': '0.01'}))
    max_price = forms.DecimalField(min_value=0, required=False, label="Максимальная цена", widget=forms.NumberInput(attrs={'step': '0.01'}))
    max_days = forms.IntegerField(min_value=0, required=False, label="Максимальное время исполнения (дни)")
    name = forms.CharField(max_length=200, required=False, label="Поиск по названию услуги")
    




class ClientSelectForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), label="Выберите клиента")



class SalonForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = ['city', 'address', 'phone', 'email', 'telegram']
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telegram': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CitySelectForm(forms.Form):
    city = forms.ChoiceField(choices=[], label="Выберите город", widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cities = Salon.objects.values_list('city', flat=True).distinct()
        self.fields['city'].choices = [(city, city) for city in cities]