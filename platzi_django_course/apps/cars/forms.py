from django import forms

from .models import Car


class AddCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('name',)


class DeleteCarForm(forms.Form):
    car_id = forms.IntegerField(min_value=0)
    
    def clean_car_id(self):
        car_id = self.cleaned_data.get('car_id')
        
        if not Car.objects.filter(id=car_id).exists():
            raise forms.ValidationError('Car with this ID does not exist.')
        return car_id
