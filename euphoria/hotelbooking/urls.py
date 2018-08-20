
from django.urls import path

from django.conf.urls.static import static

from hotelbooking.views import *
urlpatterns = [

    path('home', TemplateView.as_view(template_name = "index.html"), name = 'home'),
    path('about', TemplateView.as_view(template_name = "about.html"), name = 'about'),
    path('contact', TemplateView.as_view(template_name = 'contact.html'), name = 'contact'),
    path('location', get_hotels_by_location1, name = 'location'),
    path('location/<int:pk>/', Display_hotel_images.as_view(), name = 'display_hotel_images'),
    path('hotel_upload', hotel_upload.as_view(), name = 'hotel_upload'),
    path('hotel_list', DisplayHotelView.as_view(), name = 'hotel_list'),
    path('register/<int:pk>/', register, name = 'register'),
    path('login/<int:pk>/',loginView, name = 'login'),
    path('logout', logout_view, name = 'logout'),
    path('notfound', TemplateView.as_view(template_name = 'f_index.html'), name = 'notfound'),
    path('book_hotel/<int:pk>/', book_hotel.as_view(), name = 'book_hotel'),
    path('404', TemplateView.as_view(template_name = "404.html"), name = '404'),
    path('mybookings', mybookings, name = 'mybookings'),
    path('success', TemplateView.as_view(template_name = "congratulations.html"), name = 'success'),
    path('hotels', user_hotels, name = 'hotels'),
    path('delete_hotel/<int:pk>/', delete_hotel.as_view(), name = 'delete_hotel'),
    path('hotel_bookings/<int:pk>/', hotel_bookings.as_view(), name = 'hotel_bookings'),
    path('edit_hotel/<int:pk>/', edithotel.as_view(), name = 'edit_hotel'),
    path('feedback', feedback.as_view(), name = 'feedback'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
