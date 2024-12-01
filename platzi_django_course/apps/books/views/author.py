from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse, QueryDict

from ..models import Author
from ..forms import FullAuthorForm


class AuthorListView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        authors = Author.objects.only('id', 'name', 'birth_date').order_by('id')
        paginator = Paginator(authors, 10)

        page_number = request.GET.get('page', 1)
        authors_page = paginator.get_page(page_number)

        return render(request, 'books/author_list.html', {
            'authors_page': authors_page
        })

    def post(self, request):
        create_author_form = FullAuthorForm(request.POST)

        if create_author_form.is_valid():
            author = create_author_form.save()

            message = f'Author <{author.id}> created successfully'
            messages.success(request, message)
            return JsonResponse({
                'message': message,
                'success': True
            }, status=201)
        else:
            return JsonResponse({
                'errors': create_author_form.errors,
                'success': False
            }, status=422)


class AuthorView(View):
    http_method_names = ['put', 'delete']

    def put(self, request, id):
        try:
            put_data = QueryDict(request.body)
            author = Author.objects.get(id=id)

            author_form = FullAuthorForm(put_data, instance=author)

            if author_form.is_valid():
                author = author_form.save()

                message = f'Author <{author.id}> updated successfully'
                messages.success(request, message)
                return JsonResponse({
                    'message': message,
                    'success': True
                })
            else:
                return JsonResponse({
                    'errors': author_form.errors,
                    'success': False
                }, status=422)
        except Author.DoesNotExist:
            message = f'Author <{id}> not found'
            messages.error(request, message)
            return JsonResponse({
                'message': message,
                'success': False
            }, status=404)

    def delete(self, request, id):
        try:
            author = Author.objects.get(id=id)
            author.delete()

            message = f'Author <{id}> deleted successfully'
            messages.success(request, message)
            return JsonResponse({
                'message': message,
                'success': True
            })
        except Author.DoesNotExist:
            message = f'Author <{id}> not found'
            messages.error(request, message)
            return JsonResponse({
                'message': message,
                'success': False
            }, status=404)
