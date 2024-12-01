from django.db import models


class Publisher(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Author(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class AuthorProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    website = models.URLField(null=True, blank=True)
    biography = models.TextField(max_length=500, null=True, blank=True)
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.author


class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    publication_date = models.DateField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author, related_name='books')

    def author_ids(self, author_id):
        return self.authors.values_list('id', flat=True)

    def __str__(self):
        return self.title
