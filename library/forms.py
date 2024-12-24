from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'middle_name', 'birth_date', 'library_card_number', 'phone_number']
        widgets = {
            'birth_date': forms.DateInput(format='%d.%m.%Y', attrs={
                'class': 'form-control',
                'placeholder': 'ДД.ММ.ГГГГ',
            })
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            from datetime import date
            if birth_date > date.today():
                raise forms.ValidationError("Дата рождения не может быть в будущем.")
        return birth_date
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].input_formats = ['%d.%m.%Y']



class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Убедитесь, что это ваша модель пользователя
        fields = ['username', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'