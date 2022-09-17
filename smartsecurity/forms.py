from .models import UserRegi
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegiForm(forms.ModelForm):
    class Meta(object):
        model = UserRegi
        fields = ['name','flat','phone','email','image']

        widgets = {


            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'flat': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
              'phone': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }


            ),  'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),



        }


class CreatUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
