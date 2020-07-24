from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.db.models import F

from .forms import RegisterUserForm, LoginUserForm, TicketReservationFrom
from .models import Profile, Reservation, Passengers, Tickets, Berth


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
        return render(request, 'home/booking.html')

    def post(self, request):
        data = request.POST
        passengers_count = data.get('passenger_count', '')
        passengers_count = int(passengers_count)
        booking_form = formset_factory(TicketReservationFrom, extra=passengers_count, max_num=6, validate_max=True)
        context = {
            "form": booking_form
        }
        return render(request, 'home/reservation.html', context)


class TicketReservation(LoginRequiredMixin, View):
    login_url = '/booking'
    redirect_field_name = 'redirect_to'

    def __init__(self):
        pass

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/booking')
        ticket_form = TicketReservationFrom(request.POST)
        count = request.POST.get('form-TOTAL_FORMS', '')
        ticket_formset = formset_factory(TicketReservationFrom, extra=count)
        ticket_form = ticket_formset(request.POST)

        if ticket_form.is_valid():
            booked_status = True
            context = dict()
            context['passengers'] = list()
            # Create reservation
            reservation = Reservation()
            reservation.reserved_user = request.user
            reservation.no_of_passengers = count
            reservation.save()

            # Get condition for ladies and children
            ladies_with_children = get_ladies_with_children(ticket_form.cleaned_data)

            for each_pass in ticket_form.cleaned_data:
                passenger = Passengers()
                passenger.passenger_reservation_id = reservation
                passenger.passenger_name = each_pass.get('name', '')
                passenger.passenger_age = each_pass.get('age', '')
                passenger.passenger_gender = each_pass.get('gender', '')
                passenger.passenger_berth_preference = each_pass.get('berth_pref', '')
                old_age_passenger = get_old_age_passenger(each_pass.get('age', ''))                
                actual_berth = get_actual_berth(each_pass, old_age_passenger, ladies_with_children)
                passenger.passenger_berth_alloted = actual_berth.get('berth_id', None)
                passenger.passenger_ticket_status = actual_berth.get('ticket_status', None)
                if actual_berth.get('ticket_status', None) == 'NO_TICKET':
                    booked_status = False
                    break
                temp_dict = dict()
                temp_dict['Name'] = passenger.passenger_name
                temp_dict['Age'] = passenger.passenger_age
                temp_dict['Gender'] = passenger.passenger_gender
                try:
                    seat_details = Berth.objects.get(pk=passenger.passenger_berth_alloted)
                    temp_dict['Coach'] = seat_details.coach_name
                    temp_dict['Berth'] = seat_details.seat_name
                    temp_dict['Seat_No'] = seat_details.seat_no
                except Berth.DoesNotExist:
                    pass
                
                context['passengers'].append(temp_dict)
                passenger.save()

            if booked_status:
                context['Success'] = True

            return render(request, 'home/ticketReserved.html', context)
        else:
            print('Invalid Form')

        return redirect('/booking')


def get_ladies_with_children(passengers_list):
    child = False
    ladies = False
    for each_pass in passengers_list:
        if each_pass.get('age') < 5:
            child = True
        if each_pass.get('gender') == 'female':
            ladies = True
    
    return child and ladies


def get_old_age_passenger(passenger_age):
    if passenger_age > 60:
        return True
    return False
    

def get_actual_berth(passenger, old_age_passenger, ladies_with_children):
    return_dict = dict()
    # Tickets for children,
    if passenger.get('age', '') < 5:
        return_dict['ticket_status'] = 'FREE'        
        return return_dict

    # Check if any tickets are available,
    check_tickets = Tickets.objects.get(_id='ce8eaa214b0f4db1bd7d0f10edc67f16')

    if check_tickets.cnf_tickets <= 24:
        # Book Lower if old age or ladies with children
        if old_age_passenger or ladies_with_children:
            actual_seat = Berth.objects.order_by('seat_no').filter(is_alloted=False).filter(seat_name='L')[0]
            actual_seat.is_alloted = True
            actual_seat.save()
            check_tickets.cnf_tickets = F('cnf_tickets') + 1
            check_tickets.save()
            return_dict['berth_id'] = actual_seat.berth_id
            return_dict['ticket_status'] = 'CNF'
            return return_dict

        # Book for the Berth Preference
        for coach in ['S1', 'S2', 'S3', 'S4']:
            actual_seat = Berth.objects.order_by('seat_no').filter(is_alloted=False).filter(coach_name=coach).exclude(seat_name='SL')
            for i in actual_seat:
                if i.seat_name == passenger.get('berth_pref', ''):
                    i.is_alloted = True
                    i.save()
                    check_tickets.cnf_tickets = F('cnf_tickets') + 1
                    check_tickets.save()
                    return_dict['berth_id'] = i.berth_id
                    return_dict['ticket_status'] = 'CNF'
                    return return_dict
        
        # Book default Berth
        default_actual_seat = Berth.objects.order_by('seat_no').filter(is_alloted=False).exclude(seat_name='SL')[0]
        default_actual_seat.is_alloted = True
        default_actual_seat.save()
        check_tickets.cnf_tickets = F('cnf_tickets') + 1
        check_tickets.save()
        return_dict['berth_id'] = default_actual_seat.berth_id
        return_dict['ticket_status'] = 'CNF'
        return return_dict

    elif check_tickets.rac_tickets <= 8:
        actual_seat = Berth.objects.order_by('seat_no').filter(is_alloted=False).filter(seat_name='SL')[0]
        if actual_seat.rac_count <= 2 and actual_seat.rac_count != 0:
            check_tickets.rac_tickets = F('rac_tickets') + 1
            check_tickets.save()
            return_dict['berth_id'] = actual_seat.berth_id
            return_dict['ticket_status'] = 'RAC'
            if actual_seat.rac_count == 1:
                actual_seat.is_alloted = True
            actual_seat.rac_couunt = F('rac_count') - 1
            actual_seat.save()
            return return_dict

    elif check_tickets.waiting_tickets <= 5:
        actual_seat = Berth.objects.order_by('seat_no').filter(is_alloted=False)[0]
        check_tickets.waiting_tickets = F('waiting_tickets') + 1
        check_tickets.save()
        return_dict['berth_id'] = actual_seat.berth_id
        return_dict['ticket_status'] = 'WAITING'
        return return_dict

    else:
        return_dict['ticket_status'] = 'NO_TICKET'
        return return_dict
    
    

@login_required(login_url='/')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')