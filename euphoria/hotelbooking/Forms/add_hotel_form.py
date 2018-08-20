from django import forms
from hotelbooking.models import *
from multiupload.fields import MultiFileField


class Add_hotel(forms.ModelForm):

     class Meta:
         model = Hotel
         exclude = ['id', 'uploaded_at']


class add_hotel(forms.ModelForm):

    class Meta:
        model = Hotel
        fields = ('Hotel_Name', 'location', 'rating','no_of_rooms', 'room_price', 'Hotel_main_image', 'Hotel_images',)
        # exclude = ['id']
        widgets = {
            'Hotel_images' : forms.ClearableFileInput(attrs={'multiple': True})
        }

        # Hotel_name = forms.CharField(max_length=50)
        # location = forms.CharField(max_length=20)
        # no_of_rooms = forms.IntegerField()
        # hotel_img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        # exclude = ['id', 'uploaded_at']