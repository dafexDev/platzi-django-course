from django import forms

from .models import Publisher, Author, AuthorProfile, Book


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ('name', 'address')


class FullAuthorForm(forms.ModelForm):
    website = forms.URLField(required=False)
    biography = forms.CharField(widget=forms.Textarea, max_length=500, required=False)

    class Meta:
        model = Author
        fields = ('name', 'birth_date')

    def save(self, commit=True):
        author = super().save(commit=commit)

        profile_data = {
            'website': self.cleaned_data.get('website', ''),
            'biography': self.cleaned_data.get('biography', '')
        }

        if hasattr(author, 'profile'):
            for field, value in profile_data.items():
                setattr(author.profile, field, value)
            if commit:
                author.profile.save()
        else:
            if commit:
                AuthorProfile.objects.create(author=author, **profile_data)
            else:
                author.profile = AuthorProfile(author=author, **profile_data)
        return author


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'publication_date', 'publisher', 'authors')
