from django import forms
from .models import Account, UserProfile

#Registration Form is a class and define two fields password and confirm_password as form CharField instance
#These fields are used to capture the user's chosen password and confirm it.
# forms.PasswordInput = it mask the password as the user types it in.
# the registration form includes fields for the user's first name, last name, phone number, email,
# password, and a confirmation of the password.
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

#When the form is submitted, the clean method is called to ensure that the password and confirmation match.
#If they don't match, an error message is displayed asking the user to try again.
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match, please try again."
            )
# In the __init__ method, the placeholders for each form field are set to make it easier for the user to
# understand what they should input in each field.

    def __init__(self,*args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

# This code defines a Django form for updating the user's Account model fields for first_name, last_name, and phone_number.
# This code provides a simple way to generate a form for updating specific fields of an associated model in Django,
# while also allowing for customization of the form fields through CSS.
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self,*args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

# This part of the code provides a simple way to generate a form for updating a specific field of an associated model in Django, 
# while also allowing for customization of the form fields
#The Meta class specifies that the form is associated with the UserProfile model and should include fields for profile_picture.
class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid' : ("image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)

    def __init__(self,*args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
