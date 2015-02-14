from django import forms
from models import *
from forms import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm;

class CarTypeForm(forms.ModelForm):
    class Meta:
        model = CarType
        exclude = ('createdtime', )
        widgets = {
            'cartype' : forms.TextInput(attrs={'placeholder': 'Type...','class': 'form-control'}),
                'rentalfee' : forms.TextInput(attrs={'placeholder': '$...','class': 'form-control'}),
                    'picture' : forms.FileInput(),
            }
        error_messages = {
            'cartype': {'required':'Cartype is required'},
            'rentalfee': {'required':'Rentalfee is required'},
            'picture': {'required':'Picture is required'},
            }

    def clean_cartype(self):
        cartype=self.cleaned_data.get('cartype')
        if CarType.objects.filter(cartype__exact=cartype):
            raise forms.ValidationError("Cartype is already taken.")
        return cartype
    


class Profiles(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('owner', )
        widgets = { 'First_name':forms.TextInput(attrs={'class':'form-control','style':'width:420px',}),
                    'Last_name':forms.TextInput(attrs={'class':'form-control','style':'width:420px',}),
                    'Address_1':forms.TextInput(attrs={'class':'form-control','style':'width:420px',}),
                    'Address_2':forms.TextInput(attrs={'class':'form-control','style':'width:420px',}),
                    'City':forms.TextInput(attrs={'class':'form-control','style':'width:420px',}),
                    'State':forms.TextInput(attrs={'class':'form-control','style':'width:420px',}),
                    'Zip':forms.TextInput(attrs={'class':'form-control','style':'width:420px',}),
                    'Country':forms.TextInput(attrs={'class':'form-control','style':'width:420px',}),
                    'Phone':forms.TextInput(attrs={'class':'form-control','style':'width:420px',}),
                    'picture' : forms.FileInput() }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={
                                                        'class':'form-control',
                                                        'placeholder':'Username',
                                                        
                                                        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                                                         'class':'form-control',
                                                         'placeholder':'Password',
                                                          
                                                         }))

class ChangePass(forms.Form):
    Old_Password = forms.CharField(widget = forms.PasswordInput(attrs={
                                                           'class':'form-control',
                                                           'placeholder':'Old_Password',
                                                                'style':'width:400px'
                                                           }))
    New_Password = forms.CharField(widget = forms.PasswordInput(attrs={
                                                           'class':'form-control',
                                                           'placeholder':'New_Password',
                                                                'style':'width:400px'
                                                            }))

class FindPass(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={
                                                           'class':'form-control',
                                                           'placeholder':'Username',
                                                        #'style':'width:200px',
                                                           }))
    email = forms.EmailField(widget = forms.TextInput(attrs={
                                                           'class':'form-control',
                                                           'placeholder':'Email',
                                                      #'style':'width:200px',
                                                           }))

    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        print 'clean_username'
        if not User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is not exist.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class ResetPass(forms.Form):
    password1 = forms.CharField(widget = forms.PasswordInput(attrs={
                                                           'class':'form-control',
                                                           'placeholder':'Password',
                                                           }))
    password2 = forms.CharField(widget = forms.PasswordInput(attrs={
                                                           'class':'form-control',
                                                           'placeholder':'Confirm Password',
                                                           }))

    def clean(self):
    # Calls our parent (forms.Form) .clean function, gets a dictionary
    # of cleaned data as a result
        cleaned_data = super(ResetPass, self).clean()
        
        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        print 'clean'
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        
        # Generally return the cleaned data we got from our parent.
        return cleaned_data

class RegisterForm(forms.Form):
    username = forms.CharField(max_length = 200,
                               widget = forms.TextInput(attrs={
                                                        'class':'form-control',
                                                        'placeholder':'username',
                                                        #'style':'width:200px',
                                                        }
                                                        )
                               )
        
    email = forms.EmailField(max_length=200,
                             widget = forms.TextInput(attrs={
                                                      'class':'form-control',
                                                      'placeholder':'Email',
                                                      #'style':'width:200px',
                                                      }
                                                      )
                                                      )
    password1 = forms.CharField(max_length = 200,
                                label = 'Password',
                                widget = forms.PasswordInput(attrs={
                                                             'class':'form-control',
                                                             'placeholder':'Password',
                                                             # 'style':'width:200px',
                                                             }
                                                             )
                                                             )
    password2 = forms.CharField(max_length = 200,
                                label='Confirm password',
                                widget = forms.PasswordInput(attrs={
                                                             'class':'form-control',
                                                             'placeholder':'Confirm Password',
                                                             # 'style':'width:200px',
                                                             }
                                                             )
                                                             )
                               
                               
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegisterForm, self).clean()
                                       
        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        print 'clean'
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
                                                           
        # Generally return the cleaned data we got from our parent.
        return cleaned_data
                                                       

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        print 'clean_username'
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
    
        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username

    # Customizes form validation for the username field.
    def clean_email(self):
        # Confirms that the email is not already present in the
        # User model database.
        email = self.cleaned_data.get('email')
        print 'clean_email'
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return email

