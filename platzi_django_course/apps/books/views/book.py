from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import render
from django.http import JsonResponse, QueryDict

from ..models import Book, Publisher, Author
from ..forms import BookForm


class BookListView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        books = Book.objects.prefetch_related(
            Prefetch('authors', queryset=Author.objects.only('id'))
        ).select_related('publisher').only('id', 'title',
            'publication_date', 'publisher_id').order_by('id')
        paginator = Paginator(books, 10)

        page_number = request.GET.get('page', 1)
        books_page = paginator.get_page(page_number)

        book_with_author_ids = {
            book.id: {author.id for author in book.authors.all()}
            for book in books_page
        }

        publishers = Publisher.objects.only('id', 'name')
        authors = Author.objects.only('id', 'name')

        return render(request, 'books/list.html', {
            'books_page': books_page,
            'publishers': publishers,
            'authors': authors,
            'book_with_author_ids': book_with_author_ids
        })

    def post(self, request):
        create_book_form = BookForm(request.POST)

        if create_book_form.is_valid():
            book = create_book_form.save()

            message = f'Book <{book.id}> created successfully'
            messages.success(request, message)
            return JsonResponse({
                'message': message,
                'success': True
            }, status=201)
        else:
            return JsonResponse({
                'errors': create_book_form.errors,
                'success': False
            }, status=422)


class BookView(View):
    http_method_names = ['put', 'delete']

    def put(self, request, id):
        try:
            put_data = QueryDict(request.body)
            book = Book.objects.get(id=id)

            book_form = BookForm(put_data, instance=book)

            if book_form.is_valid():
                book = book_form.save()

                message = f'Book <{book.id}> updated successfully'
                messages.success(request, message)
                return JsonResponse({
                    'message': message,
                    'success': True
                })
            else:
                return JsonResponse({
                    'errors': book_form.errors,
                    'success': False
                }, status=422)
        except Book.DoesNotExist:
            message = f'Book <{id}> not found'
            messages.error(request, message)
            return JsonResponse({
                'message': message,
                'success': False
            }, status=404)

    def delete(self, request, id):
        try:
            book = Book.objects.get(id=id)
            book.delete()

            message = f'Book <{id}> deleted successfully'
            messages.success(request, message)
            return JsonResponse({
                'message': message,
                'success': True
            })
        except Book.DoesNotExist:
            message = f'Book <{id}> not found'
            messages.error(request, message)
            return JsonResponse({
                'message': message,
                'success': False
            }, status=404)
