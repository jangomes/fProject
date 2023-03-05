from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
# Verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from favorite.views import _fav_id
from favorite.models import Favorite,FavItem
import requests

# The register function handles user registration.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #UserProfile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            #User activation
            current_site = get_current_site(request)
            mail_subject = 'Please, activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                favorite = Favorite.objects.get(fav_id=_fav_id(request))
                is_favorite_item_exists = FavItem.objects.filter(favorite=favorite).exists()
                if is_favorite_item_exists:
                    favorite_item = FavItem.objects.filter(favorite=favorite)

# this part of the code take the favorite variation by fav id
#to group correctly when logged or not
                    product_variation = []
                    for item in favorite_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))


# here we are going to get the favorite items to access the user product variations
                    favorite_item = FavItem.objects.filter(user=user)

                    ex_var_list = []
                    id = []
                    for item in favorite_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = FavItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            favorite_item = FavItem.objects.filter(favorite=favorite)
                            for item in favorite_item:
                                item.user = user
                                item.save()

            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/favorite/senddetails/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

# It logs out the user, sets a success message, and redirects them to the login page.
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out! ')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations your account is activated!')
        return redirect('login')
    else:
        messages.error(request, 'Sorry, this is an invalid activation link.')
        return redirect('register')


# The dashboard function displays the user's dashboard page.
# It retrieves the user's UserProfile object and renders the dashboard.html template with the user's profile information.
@login_required(login_url = 'login')
def dashboard(request):

    userprofile = UserProfile.objects.get(user_id=request.user.id)

    context = {
        'userprofile' : userprofile,
    }

    return render(request, 'accounts/dashboard.html', context)

# The forgotPassword function handles password reset. When a user submits the forgot password form,
# it retrieves the user's Account object using their email address. Then, it generates a unique token
# for the password reset link and sends a password reset email to the user's email address with the link.
# The user can click on the link to reset their password.
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            #Reset password
            current_site = get_current_site(request)
            mail_subject = 'Please, reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link is expired')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')

        else:
            messages.error(request, 'Password does not match')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')

@login_required(login_url='login')
# with this code the user needs to be logged in to access the function,
# and if they're not, they will be redirected to the login page ('login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    # If the method is POST the function retrieves
    #the code creates two forms (user_form and profile_form) using the data submitted in the request.
    #These forms are used to update the user and user profile information
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated. ')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'userprofile' : userprofile,
    }
    # If the forms are valid, the code saves the updated information,
    # displays a success message and redirects the user back to the edit profile page.
    return render(request, 'accounts/edit_profile.html', context)

# This code is a function that allows users to change their passwords.
@login_required(login_url='login')
# with this code the user needs to be logged in to access the function,
# and if they're not, they will be redirected to the login page ('login')
def change_password(request):
    # If the method is POST the function retrieves the current password, new password, and confirm password entered by the user
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        # The function then gets the user object from the Account model using the current user's username.
        user = Account.objects.get(username__exact=request.user.username)

# Here if the new password and confirm password match, it sets the new password and saves it.
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match')
            return redirect('change_password')


    return render(request, 'accounts/change_password.html')
