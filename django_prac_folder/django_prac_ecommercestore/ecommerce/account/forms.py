from django import forms
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