from django.urls import path

from . import views


app_name = 'books'


urlpatterns = [
    path('', views.BookListView.as_view(), name='list'),
    path('<int:id>/', views.BookView.as_view(), name='book'),
    path('publishers/', views.PublisherListView.as_view(), name='publisher_list'),
    path('publishers/<int:id>', views.PublisherView.as_view(), name='publisher'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/<int:id>', views.AuthorView.as_view(), name='author'),
]
