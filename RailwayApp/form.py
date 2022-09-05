from django import forms
from RailwayApp.models import AdminLogin, Rail, User


class AdminLoginForm(forms.ModelForm):
    class Meta:
        model = AdminLogin
        fields = "username","password"
        labels = {
             "username": "",
             "password": ""
        } 
        widgets = {
            "username":  forms.TextInput(attrs={'placeholder':'Enter Username','autocomplete': 'off', 'class': 'form-control'}), 
            "password": forms.PasswordInput(attrs={'placeholder':'Enter Password','autocomplete': 'off','data-toggle': 'password', 'class': 'form-control'}),
        }

class RailForm(forms.ModelForm):
    class Meta:
        model = Rail
        fields = "__all__"
        labels = {
             "name": "",
             "fromAddress": "",
             "toAddress": "",
             "price": "",
             "duration": "",
             "date": "",
             "time": "",
        } 
        widgets = {
            "name":  forms.TextInput(attrs={'placeholder':'Enter Train Name','autocomplete': 'off', 'class': 'form-control'}), 
            "fromAddress":  forms.TextInput(attrs={'placeholder':'Enter From Address','autocomplete': 'off', 'class': 'form-control'}), 
            "toAddress":  forms.TextInput(attrs={'placeholder':'Enter To Address','autocomplete': 'off', 'class': 'form-control'}), 
            "price":  forms.TextInput(attrs={'placeholder':'Enter Ticket Price','autocomplete': 'off', 'class': 'form-control'}), 
            "duration":  forms.TextInput(attrs={'placeholder':'Enter Travel Duration','autocomplete': 'off', 'class': 'form-control'}), 
            "date":  forms.TextInput(attrs={'placeholder':'Enter Departure Date','autocomplete': 'off', 'class': 'form-control'}), 
            "time":  forms.TextInput(attrs={'placeholder':'Enter Departure Time','autocomplete': 'off', 'class': 'form-control'}), 
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        labels = {
             "username": "",
             "password": "",
             "firstname": "",
             "lastname": "",
             "email": "",
             "contact": "",
             "image_url": "",
        }
        widgets = {
            "firstname":  forms.TextInput(attrs={'placeholder':'Enter First Name','autocomplete': 'off', 'class': 'form-control'}),
            "lastname":  forms.TextInput(attrs={'placeholder':'Enter Last Name','autocomplete': 'off', 'class': 'form-control'}),
            "username":  forms.TextInput(attrs={'placeholder':'Enter Username','autocomplete': 'off', 'class': 'form-control', 'id': 'userName'}),
            "password": forms.PasswordInput(attrs={'placeholder':'Enter Password','autocomplete': 'off','data-toggle': 'password', 'class': 'form-control'}),
            "email":  forms.TextInput(attrs={'placeholder':'Enter Email Address','autocomplete': 'off', 'class': 'form-control', 'id': 'emailVerify'}),
            "contact":  forms.TextInput(attrs={'placeholder':'Enter Contact No.','autocomplete': 'off', 'class': 'form-control'}),
        }


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "username","password"
        labels = {
             "username": "",
             "password": ""
        }
        widgets = {
            "username":  forms.TextInput(attrs={'placeholder':'Enter Username','autocomplete': 'off', 'class': 'form-control'}), 
            "password": forms.PasswordInput(attrs={'placeholder':'Enter Password','autocomplete': 'off','data-toggle': 'password', 'class': 'form-control'}),
        }