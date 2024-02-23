from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import RegistrationForm
from .token import account_activation_token

# Create your views here.
def account_register(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        registerform = RegistrationForm(request.POST)

        """
        Q: What is 'is_valid'?
        A: The 'is_valid' method performs all the validation rules set on the form fields, 
           including any custom validations we have defined. If the data passes all the validations, 
           'is_valid' returns True, and the validated data is stored in the 'cleaned_data' dictionary.
        """
        if registerform.is_valid():
            
            """
            Q: Why save(commit=False)?
            A: To process some additional things before being saved to the database. 'commit=False' 
               argument tells django to create a model instance from the validated form data 
               but not to save it to the database yet. This allows us to add or modify attributes 
               of the model instance before actually saving it. In this case, we don't want to 
               map our form to 'UserBase' data-table since we want to check whether submitted data
               is cleaned. So we saving form, but not directly commited to our model right away. 
            """
            user = registerform.save(commit=False)

            # 'cleaned_data' is attribute of form instance that stores the sanitized and 
            # validated data once a form has been submitted. This attribute becomes available 
            # after we call the 'is_valid' method on our form instance. It can detect and clean
            # injected code, or other harmful things from data that is submitted.
            user.email = registerform.cleaned_data['email']
            user.set_password = registerform.cleaned_data['password']

            # To make them activate themselves through their email
            user.is_active = False
            
            # Now map(save) this form to 'UserBase' model. It means now new 'UserBase' instance is
            # created(new row is added in 'UserBase' data-table) based on data submitted through form.
            user.save()

            current_site = get_current_site(request)
            subject = "Activate your Account!"

            # Load template and pass the template the context, which is given as dictionary.
            # So user would get given template that contains given contexts
            # through their email when they register, as part of account activation process.
            message = render_to_string('account/registration/account_activation_email.html',
                                       {
                                           'user':user,
                                           'domaim':current_site.domain,
                                           'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token':account_activation_token.make_token(user),
                                       })
            
            # 'email_user' method of "UserBase" model will be made later.
            user.email_user(subject=subject, message=message)

