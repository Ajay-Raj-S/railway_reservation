from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import JsonResponse

from .forms import RegisterUserForm, LoginUserForm, TicketReservationFrom
from .models import Profile


class Home(View):
    """
        Home contains the Login Form
    """
    def __init__(self):
        pass

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/booking")
        login_form = LoginUserForm()
        context = {
            "form": login_form
        }
        return render(request, 'home/home.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("/booking")
        login_form = LoginUserForm(request.POST)
        if login_form.is_valid():            
            data = login_form.cleaned_data
            try: 
                user = User.objects.get(username=data['user_name'])
                user_authenticated = auth.authenticate(
                    username=data['user_name'],
                    password=data['password']
                )
                if user_authenticated is not None:
                    auth.login(request, user)
                    return redirect('booking/')
                else:
                    messages.error(request, 'Username or password is incorrect!')
                    return redirect('/')
            except User.DoesNotExist:
                messages.error(request, 'user doesn\'t exist!')
                return redirect('/')
        messages.error(request, 'Invalid Form data')
        return redirect('/')


class Register(View):
    def __init__(self):
        pass
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/booking")
        register_form = RegisterUserForm()
        context = {
            "form": register_form
        }
        return render(request, 'home/register.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("/booking")
        register_form = RegisterUserForm(request.POST)
        if register_form.is_valid():
            data = register_form.cleaned_data
            try: 
                user = User.objects.get(username=data['user_name'])
                messages.error(request, "Username or email exists")
                return redirect('/register')
            except User.DoesNotExist:
                pass
            
            try: 
                user = User.objects.get(email=data['email_id'])                
                messages.error(request, "Username or email exists")
                return redirect('/register')
            except User.DoesNotExist:
                pass

            user = User.objects.create_user(
                            username=data['user_name'],
                            email=data['email_id'],
                            password=data['password'],
                            first_name=data['first_name'],
                            last_name=data['last_name']
                        )
            user.save()
            user.refresh_from_db()
            user = User.objects.get(username=data['user_name'])
            user_profile = Profile()
            user_profile.gender = data['gender']
            user_profile.age = data['age']
            user_profile.user = user
            user_profile.save()
            messages.info(request, 'Login with your username and password')
            return redirect('/')
        
        # if the form is Invalid
        messages.error(request, 'Invalid Form')
        return redirect('/register')


class Booking(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def __init__(self):
        pass

    def get(self, request):        
        booking_form = formset_factory(TicketReservationFrom, extra=6)
        context = {
            "form": booking_form
        }
        return render(request, 'home/booking.html', context)

    def post(self, request):
        booking_form = TicketReservationFrom(request.POST)
        if booking_form.is_valid():
            data = booking_form.cleaned_data
            print(data)
            return render(request, "home/booked.html")
        else:
            messages.error(request, "Invalid Form!")
            return redirect("/booking")


@login_required(login_url='/')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')