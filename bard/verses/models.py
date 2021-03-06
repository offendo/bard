from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from vote.models import VoteModel

# import mptt
from mptt.models import MPTTModel, TreeForeignKey
# from mptt.fields import TreeForeignKey
from django.contrib.auth.models import Group

# Create your models here.
def get_sentinel_user():
    ''' Gets anonymous user when a user is deleted
    '''
    return get_user_model().objects.get_or_create(username='Anonymous')[0]

class Genre(models.Model):
    ''' Stores a list of genres
    '''
    name = models.CharField(null=False, max_length=30)


class Verse(VoteModel, MPTTModel):
    body          = models.TextField(max_length=300)
    parent        = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE, db_index=True)
    author        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    creation_date = models.DateTimeField(default=timezone.now)
    genre         = models.ManyToManyField(Genre)
    max_mean_score     = models.DecimalField(decimal_places=2, max_digits=3, default=0)
    
    def __str__(self):
        return str(self.id) + ': ' + str(self.body)[:10] + '...'

    class Meta:
        ordering = ['-num_vote_up']

class Weights(models.Model):
    name = models.ManyToManyField(Genre)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    value = models.DecimalField(decimal_places=2, max_digits=5, default=0)
