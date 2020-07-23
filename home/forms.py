from django import forms

gender_choices = ( 
    ("male", "Male"), 
    ("female", "Female"), 
    ("others", "Others"),
)

berth_choices = (
    ("L", "Lower"),
    ("M", "Middle"),
    ("U", "Upper"),
    ("SU", "Side Upper"),
)

class RegisterUserForm(forms.Form):   
    first_name = forms.CharField(max_length=64, label='First Name', required=True)
    last_name = forms.CharField(max_length=64, label='Last Name', required=True)
    user_name = forms.CharField(max_length=64, label='User Name', required=True)    
    email_id = forms.EmailField(label='Email address')
    password = forms.CharField(max_length=32, label='Password', required=True, help_text='Password should be Minimum of 8 characters.', widget=forms.PasswordInput)
    age = forms.IntegerField(label='Age', max_value=130, min_value=1)
    gender = forms.ChoiceField(choices=gender_choices, required=True)


class LoginUserForm(forms.Form):
    user_name = forms.CharField(max_length=64, label='User Name', required=True)
    password = forms.CharField(max_length=32, label='Password', required=True, widget=forms.PasswordInput)


class TicketReservationFrom(forms.Form):
    name = forms.CharField(max_length=128, label='Full Name', required=True)
    age = forms.IntegerField(label='Age', max_value=130, min_value=1)
    gender = forms.ChoiceField(choices=gender_choices)
    berth_pref = forms.ChoiceField(choices=berth_choices, required=True)