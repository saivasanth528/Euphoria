from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from hotelbooking.Forms import *
from hotelbooking.models import *
from django.views.generic import *
from django.core.mail  import send_mail
import smtplib
from django.contrib.auth import authenticate, login

from django.contrib.auth import logout
from django.views.generic.edit import FormView
import os
from django.conf import settings


from django.contrib import messages
# import datetime as dt
from datetime import datetime as dt
# Create your views here.
def register(request, *args, **kwargs):

    # import ipdb
    # ipdb.set_trace()
    user_type = int(kwargs['pk'])

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']

            if not (Hotel_users.objects.filter(username=username).exists() or Hotel_users.objects.filter(email=email).exists()):
                if user_type == 1:
                    Hotel_users.objects.create_user(username, email, password, isHotel_representative = True)
                    user = authenticate(username=username, password=password, isHotel_representative = True)
                else:
                    Hotel_users.objects.create_user(username, email, password, isHotel_representative = False)
                    user = authenticate(username=username, password=password, isHotel_representative=False)

                login(request, user)
                return redirect(reverse_lazy('home'))
            else:
                messages.error(request, message="Looks like username or email already exists , please choose another :)")
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form' : form})


def loginView(request, *args, **kwargs):

    id = int(kwargs['pk'])

    if request.method == 'GET':
        context = {'id' : id}
        return render(
            request,
            template_name='registration/login.html',
            context = context
        )

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usr=Hotel_users.objects.filter(username=username)
        if len(usr) == 0:
            messages.error(request, message="Invalid username/password")
            return render(request, template_name='registration/login.html', context={'id': id})
        user_type = bool(id)
        if user_type==usr[0].isHotel_representative:
            user = authenticate(username=username, password=password, isHotel_representative = user_type)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('home'))
        else:
            messages.error(request, message="Invalid username/password")
            return render(request, template_name='registration/login.html',context={'id':id})

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def get_hotels_by_location1(request):


    location = request.POST.get('location')
    try:
        location = location.lower()
    except AttributeError as e:
        redirect('404')
    # check_in_date = request.POST.get('check_in')
    # check_out_date = request.POST.get('check_out')
    # adults = request.POST.get('adult')
    # children = request.POST.get('children')

    hotels = Hotel.objects.filter(location=location)
    if len(hotels) == 0:
        title = 'No hotels'
        heading = 'Sorry no hotels found on your location'
        content = 'You can add your own hotels on your location by signing in as hotel representative'

        return render(
            request,
            template_name = 'f_index.html',
            context = {'heading' : heading, 'content' : content, 'title' : title}
        )

    # Hotel_search.objects.all().delete() #Deleting all previous searches, to get the search based on recent one in booking room
    # check_in_date = dt.strptime(check_in_date, '%m/%d/%Y').strftime('%Y-%m-%d')
    # check_out_date = dt.strptime(check_out_date, '%m/%d/%Y').strftime('%Y-%m-%d')
    # Hotel_search.objects.create(location = location, check_in = check_in_date, check_out = check_out_date, adults = adults, children = children,
    #                             user = request.user)

    k = 0
    for k in range(len(hotels)):
        hotels[k].rating = list(range(int(hotels[k].rating)))

    context = {'hotels': hotels}
    return render(
        request,
        template_name='display_hotel_by_location1.html',
        context=context
    )

class Display_hotel_images(ListView):


    context_object_name = 'hotel_images'
    template_name = 'display_hotel_images.html'
    model = Hotel_image

    def get_context_data(self,**kwargs):

        context = super(Display_hotel_images, self).get_context_data(**kwargs)
        hotel_id = int(self.kwargs['pk'])
        hotel_images = Hotel_image.objects.filter(hotel__id = hotel_id)
        context ['hotel_images'] = hotel_images
        context['hotel_id'] = hotel_id
        return context



class DisplayHotelView(ListView):

    def get(self, request):

        result = Hotel.objects.all()
        context = {'hotels': result, 'header': ['Hotel_Name', 'location', 'price', 'stars', 'image'] }
        return render(
            request,
            template_name='display_hotels.html',
            context = context
        )


class hotel_upload(LoginRequiredMixin,FormView):

    login_url = '/login'
    template_name = 'photos/basic_upload/index.html'
    model = Hotel
    form_class = add_hotel
    # success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):

        form = add_hotel
        return render(
                self.request,
                template_name = self.template_name,
                context={'form' : form}
             )

    def post(self, request, *args, **kwargs):

        form = self.form_class(self.request.POST, self.request.FILES)
        if form.is_valid():

            Hotel_Name = form.cleaned_data['Hotel_Name']
            location = form.cleaned_data['location']
            no_of_rooms = form.cleaned_data['no_of_rooms']
            room_price = form.cleaned_data['room_price']
            rating = form.cleaned_data['rating']
            hotel_main_image = form.cleaned_data['Hotel_main_image']
            hotel_images = form.cleaned_data['Hotel_images']
            # now = dt.datetime.now()
            # uploaded_at = now.strftime("%Y-%m-%d %H:%M:%S")
            user = request.user

            hotel_object = Hotel.objects.create(Hotel_Name = Hotel_Name, location = location, no_of_rooms = no_of_rooms, room_price = room_price, rating = rating,
                                                Hotel_main_image = hotel_main_image,  user = user)

            # import ipdb
            # ipdb.set_trace()
            hotel_images_list = form.files.getlist('Hotel_images')
            for image in hotel_images_list:
                p = Hotel_image.objects.create(hotel_img = image, hotel = hotel_object)
                p.save()

            heading = 'Congratulations you succesfully added a hotel'
            content = 'You can see your hotel bookings by clicking on a bookings link '
            try:
                content1 = "you have successfully added your hotel through euphoria bookings, you can see " \
                           " your hotel bookings by clicking on a bookings link,  Have a nice business :)"

                msg_html = render_to_string('email_template.html', {'user': user.username, 'content': content1})
                send_mail('Booking Confirmation', msg_html, 'euphoriareservation@gmail.com', [user.email],
                          html_message=msg_html,
                          fail_silently=False)
            except Exception as e:
                pass

            return render(
                request,
                template_name = 'congratulations.html',
                context = {'heading' : heading, 'content' : content}
            )

        return render(request, self.template_name, {'form': form})




class book_hotel(LoginRequiredMixin, FormView):
    login_url = '/login'
    template_name = 'room_book.html'
    #model = Customer_details
    #form_class = hotel_book
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):

            hotel_id = int(self.kwargs['pk'])
            price = Hotel.objects.values('room_price').get(id = hotel_id)
            room_price  = price['room_price']
            return render(
                self.request,
                template_name=self.template_name,
                context={'amount': room_price}
            )

    def post(self, request, *args, **kwargs):

        hotel_id = int(self.kwargs['pk'])
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        proof_id = request.POST.get('proof_id')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        people = request.POST.get('no_of_people')
        rooms = request.POST.get('no_of_rooms')
        amount = request.POST.get('amount')
        special_request = request.POST.get('special_request')
        user = request.user

        customer_details = Customer_details.objects.create(Name = name, Age = age, Mobile_number = phone, Email = email, proof_id = proof_id,
                                                           user = user)
        customer_details.save()
        hotel_details = Hotel.objects.values('Hotel_Name', 'location').get(id=hotel_id)

        booking_details = Booking_details.objects.create(hotel_name = hotel_details['Hotel_Name'], location = hotel_details['location'],
                                                         check_in_date = check_in, check_out_date = check_out, amount = amount,
                                                         no_of_rooms = rooms, customer = customer_details,Number_of_guests = people,
                                                         Special_request = special_request, user = user, hotel_id = hotel_id)
        booking_details.save()

        heading = 'Congratulations you succesfully booked a hotel'
        content = 'You can see your hotel bookings by clicking on a bookings link , the hotel representative will' \
                  ' contact you soon and you can pay through his payement method'

        try:
            content1 = "you have successfully booked the hotel through euphoria bookings, the hotel representative " \
                       " will contact you soon about payement method and other offers, Have a good trip :)"
            msg_html = render_to_string('email_template.html', {'user': user.username, 'content' : content1 })
            send_mail('Booking Confirmation', msg_html, 'euphoriareservation@gmail.com', [email, user.email],html_message=msg_html,
                      fail_silently=False)
        except Exception as e:
            pass
        return render(
            request,
            template_name='congratulations.html',
            context={'heading': heading, 'content': content}
        )


def mybookings(request):

    booking_details = Booking_details.objects.values('hotel_name', 'location', 'check_in_date', 'check_out_date',
                                                     'no_of_rooms', 'Number_of_guests', 'amount').filter(user = request.user)
    if len(booking_details) == 0:
        title = 'No bookings'
        header = 'Sorry currently there are no bookings for you'
        content = 'You can book the desired hotel on your location if exists :), you can also' \
                  ' add hotel by signing as hotel representative'
        return render(
            request,
            template_name = 'f_index.html',
            context = {'heading' : header, 'content' : content, 'title' : title}
        )

    header = ['Hotel Name', 'location', 'check_in', 'check_out','Rooms', 'Guests', 'Amount']
    return render(
        request,
        template_name = 'display_bookings.html',
        context={'bookings' : booking_details, 'header' : header}
    )

def user_hotels(request):

    user = request.user
    hotels = Hotel.objects.filter(user = user)
    if len(hotels) == 0:
        title = 'No hotels'
        heading = 'Sorry no hotels found for you'
        content = "You can add your own hotels by clicking on 'addHotel' in Home page"
        return render(
            request,
            template_name='f_index.html',
            context={'heading': heading, 'content': content, 'title' : title}
        )
    k = 0
    for k in range(len(hotels)):
        hotels[k].rating = list(range(int(hotels[k].rating)))

    context = {'hotels': hotels}
    return render(
        request,
        template_name='user_hotels.html',
        context=context
    )

class delete_hotel(LoginRequiredMixin, DeleteView):

    login_url = '/login'
    def get(self, request, *args, **kwargs):

        hotel_id = int(self.kwargs['pk'])
        hotel = Hotel.objects.get(id = hotel_id)
        hotel_images = Hotel_image.objects.filter(hotel__id=hotel_id)
        if hotel.Hotel_main_image.name:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(hotel.Hotel_main_image.name)))
                for image in hotel_images:
                    os.remove(os.path.join(settings.MEDIA_ROOT, image.hotel_img.name))
            except OSError:
                pass

        hotel.delete()
        return redirect('hotels')



class hotel_bookings(LoginRequiredMixin,ListView):

    login_url = '/login'

    def get(self, request, *args, **kwargs):

        hotel_id = int(self.kwargs['pk'])
        booking_details = Booking_details.objects.values('customer__Name', 'customer__Age','customer__Mobile_number',
                                                         'customer__Email', 'check_in_date', 'check_out_date',
                                                         'no_of_rooms', 'Number_of_guests', 'amount').filter(hotel_id = hotel_id)
        if len(booking_details) == 0:
            title = 'No bookings'
            heading = 'Sorry no bookings found for your hotel'
            content = "Hope we can see the bookings in future , for the time being plan new offers :)"
            return render(
                request,
                template_name='f_index.html',
                context={'heading': heading, 'content': content, 'title' : title}
            )

        header = ['Name','Age', 'Mobile Number', 'Email', 'check_in', 'check_out', 'Rooms', 'Guests', 'Amount']
        return render(
            request,
            template_name='display_bookings.html',
            context={'bookings': booking_details, 'header': header}
        )



class edithotel(LoginRequiredMixin,ListView):

    login_url = '/login'
    def get(self, request, *args, **kwargs):
        title = 'under construction'
        header = 'This feature is under construction'
        content = 'Please be patient , this feature will be added soon with more options, Sorry for inconvenience :)'
        return render(
            request,
            template_name='f_index.html',
            context={'heading': header, 'content': content, title : title}
        )


class feedback(LoginRequiredMixin, ListView):

    login_url = '/login'
    def get(self, request, *args, **kwargs):

        title = 'Feedback'
        header = 'Thanks for your feedback'
        content = 'We will take the corresponding action and contact you soon, if anything wrong we will improve our site :)'
        return render(
            request,
            template_name='f_index.html',
            context={'heading': header, 'content': content, title : title}
        )
