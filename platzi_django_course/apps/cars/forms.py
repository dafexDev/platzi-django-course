from django import forms
import datetime

from .models import Car


class AddCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('name','year')
        
    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year is not None:
            if year < 1886: # First car year
                raise forms.ValidationError("The year cannot be earlier than 1886.")
            if year > datetime.date.today().year:
                raise forms.ValidationError("The year cannot be in the future.")
        return year


class DeleteCarForm(forms.Form):
    car_id = forms.IntegerField(min_value=0)
    
    def clean_car_id(self):
        car_id = self.cleaned_data.get('car_id')
        
        if not Car.objects.filter(id=car_id).exists():
            raise forms.ValidationError('Car with this ID does not exist.')
        return car_id
