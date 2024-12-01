from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse, QueryDict

from platzi_django_course.apps.common.views.generic import MethodOverrideMixin

from ..models import Publisher
from ..forms import PublisherForm


class PublisherListView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        publishers = Publisher.objects.only('id', 'name', 'address').order_by('id')
        paginator = Paginator(publishers, 10)

        page_number = request.GET.get('page', 1)
        publishers_page = paginator.get_page(page_number)

        return render(request, 'books/publisher_list.html', {
            'publishers_page': publishers_page
        })

    def post(self, request):
        create_publisher_form = PublisherForm(request.POST)

        if create_publisher_form.is_valid():
            publisher = create_publisher_form.save()

            message = f'Publisher <{publisher.id}> created successfully'
            messages.success(request, message)
            return JsonResponse({
                'message': message,
                'success': True
            }, status=201)
        else:
            return JsonResponse({
                'errors': create_publisher_form.errors,
                'success': False
            }, status=422)


class PublisherView(MethodOverrideMixin, View):
    http_method_names = ['put', 'delete']

    def put(self, request, id):
        try:
            put_data = QueryDict(request.body)
            publisher = Publisher.objects.get(id=id)

            publisher_form = PublisherForm(put_data, instance=publisher)

            if publisher_form.is_valid():
                publisher = publisher_form.save()

                message = f'Publisher <{publisher.id}> updated successfully'
                messages.success(request, message)
                return JsonResponse({
                    'message': message,
                    'success': True
                })
            else:
                return JsonResponse({
                    'errors': publisher_form.errors,
                    'success': False
                }, status=422)
        except Publisher.DoesNotExist:
            message = f'Publisher <{id}> not found'
            messages.error(request, message)
            return JsonResponse({
                'message': message,
                'success': False
            }, status=404)

    def delete(self, request, id):
        try:
            publisher = Publisher.objects.get(id=id)
            publisher.delete()

            message = f'Publisher <{id}> deleted successfully'
            messages.success(request, message)
            return JsonResponse({
                'message': message,
                'success': True
            })
        except Publisher.DoesNotExist:
            message = f'Publisher <{id}> not found'
            messages.error(request, message)
            return JsonResponse({
                'message': message,
                'success': False
            }, status=404)
