from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
def get_sentinel_user():
    ''' Gets anonymous user when a user is deleted
    '''
    return get_user_model().objects.get_or_create(username='Anonymous')[0]

class Genre(models.Model):
    ''' Stores a list of genres
    '''
    name = models.CharField(null=False, max_length=30)

class Verse(models.Model):
    ''' Verse model containing the following attributes:
        ID: id of verse
        Body: Actual text
        Score: Rating
        Parent: Parent verse (null if it's a base)
        Author: Who wrote the verse
        Creation date: Authorship date.
    '''
    body = models.TextField(max_length=300)
    score = models.IntegerField(default=0)
    parent = models.ForeignKey('Verse', null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    creation_date = models.DateTimeField(default=timezone.now)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.author + '.' + super.ID + '=' + str(self.body).split(' ')[:15] + '...'
