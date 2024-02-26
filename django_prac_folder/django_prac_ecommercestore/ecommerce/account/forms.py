from django import forms
from django.contrib.auth.forms import (AuthenticationForm)

from .models import UserBase

class RegistrationForm(forms.ModelForm):

    """
    Q: So, there is many kinds of form classes, why use ModelForm in this case?
    A: In django, ModelForm is directly linked to model we specify in model attribute of Meta class,
       and ModelForm can perform operations directly on instances of that specified model. And it 
       follows these steps when dealing User model in form : 
       1. Validates the form data against the model to ensure that it fits all the constraints 
       and validations defined in the model (and any additional form validations we may have added).
       2. If the form data is valid, Django creates a new instance of the User model with the 
       form's input data. This includes setting the User model's fields to the values provided 
       in the form.
       3. Django then saves this new User instance to the database, creating a new record.
       4. The save() method returns the newly created User instance, which we assign to the 
       variable user.
       So when we look at views.py and see 'account_register' function,
       'user = registerForm.save()' essentially creates new 'UserBase' instance in the database 
       with the details submitted via the form, assuming that all form fields are valid. 
       This process makes handling user input and creating new records in the database.
    """

    user_name = forms.CharField(label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        
        """
        Q: Why not just 'r.exists'? What is difference between 'r.count'?
        A: They both doing similar thing in this case, since we are just checking whether
           form data that is sent by user is already exist in database or not. So
           'r.count' return number of objects we are looking for. However they
           actually work different, 'r.count' counts how many objects are found in database.
           On the other hand, 'r.exists' check whether object we are looking for exists in database.
        """
        r = UserBase.objects.filter(user_name=user_name) 
        if r.count():
            
            raise forms.ValidationError("Username is already exists")
        return user_name
    
    # def clean_password(self):
    #     password1 = self.cleaned_data['password']

    # # 'password2' isn't present in cleaned_data, so 'password2' is set to None
    #     password2 = self.cleaned_data['password2']

    #     if password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2

    """
    Q: When function name is clean_password, why function causing keyerror:password2?
    A: The reason behind is django form convention. Since 'password2' field comes later(after)
       'password' field, we need to write 'clean_password2'. Because 'password' comes before 
       'password2' in the fields list, when 'clean_password' is run, cleaned_data["password2"] has not
        yet been set. To be more specific, the method 'clean_<fieldname>()' is a django convention 
        for adding custom validation logic to a specific form field. The naming convention 
        'clean_password2' implies that this method specifically validates the 'password2' field. 
        Django doesn't automatically check if 'password' and 'password2' match. We have to implement 
        this logic ourselves, which is done in the 'clean_password2' method. Ok then, why the method 
        isn't named 'clean_password' if it's validating the password. The reason is that django 
        processes form fields in the order they are declared and calls the 'clean_<fieldname>()' 
        method for each field. So 'clean_password2' naming suggest that we are now in the process of
        dealing 'password2' field validation. It means 'clean_password' function (if it exists) has 
        already run and 'password' is valid by itself. The 'clean_password2' method can then focus 
        on comparing 'password' to 'password2'.
    """
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Please use another email, that is already exists")
        return email
    

    # This function initialize styles for forms(input-form). 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Names of classes are from bootstrap
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


# This form exists to overriding or bringing django's default forms of 'AuthenticationForm'
# and just changes styling. If we see 'LoginView' there is 'AuthenticationForm'. We are overriding
# it. Since 'LoginView' or 'LogoutView' implementing 'AuthenticationForm' inside(it is instantiated)
# we don't need to make logic for login/out process unless we are making our custom logic.
class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-3', 
            'placeholder': 'Username', 
            'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',}))


# This form exists to make form for user information editing. 
class UserEditForm(forms.ModelForm):

    # Since form attribute, 'readonly' is enabled, user can see 'email' and 'user_name' appears their
    # editing form. But they can't update it. 
    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))
    user_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname', 'readonly': 'readonly'}))
    
    first_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-lastname'}))

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'first_name',)

    # When user editing his/her informations, 'user_name' and 'email' is required. 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True