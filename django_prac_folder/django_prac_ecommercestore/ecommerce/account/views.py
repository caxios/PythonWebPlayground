from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponse

from .forms import RegistrationForm, UserEditForm
from .token import account_activation_token
from .models import UserBase

@login_required
def dashboard(request):
    return render(request, 'account/user/dashboard.html')

@login_required
def edit_details(request):
    user_form = UserEditForm()
    
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, "account/user/edit_details.html", {"user_form":user_form})

def account_register(request):

    # if request.user.is_authenticated:
    #     return redirect('/')

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

            # 'set_password' is a method of django's 'User' model
            user.set_password = registerform.cleaned_data['password']

            # To make them activate themselves through their email that handles password hashing 
            # before saving it to the database
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
            return HttpResponse("Successfully registered!")
    else:
        registerform = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form':registerform})

# User is activated via this view function. 
def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
        
        if user is not None and account_activation_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('account:dashboard')
        else:
            return render(request, 'account/registration/activation_invalid.html')
    except:
        print("error")