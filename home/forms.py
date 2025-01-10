from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput,PasswordInput, ModelForm
from django import forms
from django.contrib.auth.hashers import make_password




class UserAddForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']
        
        widgets = {
            "first_name":TextInput(attrs={"class":"form-control  py-3","placeholder":"First Name"}),
            "username":TextInput(attrs={"class":"form-control  py-3","placeholder":"Username"}), 
            "email":TextInput(attrs={"class":"form-control py-3","placeholder":"Email Id"}),    
        }  
        
    def __init__(self, *args, **kwargs):
        super(UserAddForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control  py-3', 'placeholder': 'Password'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control  py-3', 'placeholder': 'Password confirmation'})

class UserUpdateForm(UserChangeForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput, help_text="Leave blank if not changing.")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.password = make_password(password)
        if commit:
            user.save()
        return user
    

from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }



from .models import Products, Vaccinations

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ['user']  # Include all fields from the model
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description'}),
            'pet': forms.Select(attrs={'class': 'form-select form-control'}),
            'category': forms.Select(attrs={'class': 'form-select form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock quantity'}),
        }

from django import forms
from .models import BookAppointment, Pet
from datetime import date

class BookAppointmentForm(forms.ModelForm):
    class Meta:
        model = BookAppointment
        exclude = ['hospital', 'user',"status"]  # Exclude hospital and user fields
        widgets = {
            'booking_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'pet': forms.Select(attrs={'class': 'form-control'}),
            'treatment': forms.Select(attrs={'class': 'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set form-control class for all fields by default
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') != 'form-check-input':
                field.widget.attrs['class'] = 'form-control'

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date and booking_date.date() < date.today():
            raise forms.ValidationError("Booking date cannot be in the past.")
        return booking_date
    


class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccinations
        exclude = ['hospital']  # Exclude the hospital field
        widgets = {
            'date_added': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'date_updated': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'vaccine_type': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'pet': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set form-control class for all fields that are not explicitly set
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') is None:
                field.widget.attrs['class'] = 'form-control'



class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        exclude = ['owner']  # Exclude the owner field
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'pet_type': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add 'form-control' class to all fields that are not explicitly set
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'