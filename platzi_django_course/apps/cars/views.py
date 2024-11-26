from django.shortcuts import render, redirect

from .forms import AddCarForm, DeleteCarForm
from .models import Car


def car_list(request):    
    context = {}
    
    if request.method == 'POST':
        delete_form = DeleteCarForm(request.POST)
        if delete_form.is_valid():
            car_id = delete_form.cleaned_data['car_id']
            Car.objects.filter(id=car_id).delete()
    else:
        delete_form = DeleteCarForm()
        
    car_list = Car.objects.all()
        
    context['delete_form'] = delete_form
    context['car_list'] = car_list
    
    return render(request, 'cars/car_list.html', context)


def add_car(request):
    if request.method == 'POST':
        form = AddCarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = AddCarForm()
    
    return render(request, 'cars/add_car.html', {
        'form': form
    })
