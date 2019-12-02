from django.shortcuts import render, redirect
from .models import Verse, Genre
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView
from collections import Counter



# utility functions 
def adjust_score(request, url):# {{{
    if request.method == 'POST':
        new_id = request.POST['obj_id']
        new_obj = Verse.objects.get(id=new_id)
        if request.POST['score'] == '+1':
            if not new_obj.votes.exists(user_id=request.user.id):
                new_obj.votes.up(user_id=request.user.id)
                new_obj.num_vote_up += 1
        elif request.POST['score'] == '-1':
            if new_obj.votes.exists(user_id=request.user.id):
                new_obj.votes.down(user_id=request.user.id)
                new_obj.num_vote_up ^= 1
        new_obj.save()
        # update root's max_score
        root = new_obj.get_root()
        root.max_mean_score = get_max_mean_score(root)
        root.save()

    return HttpResponseRedirect(url)# }}}

def sort_tree(sorted_items, items, root):# {{{
    sorted_items.append(root)
    children = items.filter(parent_id=root.id)
    if not children:
        return sorted_items
    children = sorted(children, key=lambda x: x.votes.count(), reverse=True)
    for item in children:
        sorted_items = sort_tree(sorted_items, items, item)
    return sorted_items# }}}

def get_max_mean_score(root):# {{{
    descs = root.get_descendants(include_self=False)
    max_mean = 0
    for desc in descs:
        if desc.is_leaf_node():
            ancs = desc.get_ancestors(include_self=True)
            mean = sum(a.votes.count() for a in ancs) / len(ancs)
            if mean > max_mean:
                max_mean = mean
    return max_mean# }}}

# Create your views here.
@login_required(login_url='/accounts/login')
def verse_detail_view(request, id):
    this = Verse.objects.get(id=id)
    # new_verse.genre.set(genres)
    adjust_score(request, f'verses/{id}')
    items = Verse.objects.all().filter(tree_id=this.tree_id)
    sorted_items = sort_tree([], items, items.get(parent_id=None))
    context = {'nodes':sorted_items}
    return render(request, "verses/verse.html", context)

@login_required(login_url='/accounts/login')
def verse_new_story_view(request):
    # adjust_score(request)
    if request.method == 'POST':
        form = NewVerseForm(request.POST)
        if form.is_valid():
            author = User.objects.get(id=request.user.id)
            post = dict(request.POST.lists())
            genre_list = set(post['genre'])
            genres = Genre.objects.all().filter(name__in=genre_list)
            story  = request.POST['story']
            new_verse = Verse(body=story, parent=None, author=author)
            new_verse.save()
            new_verse.genre.set(genres)
            new_verse.save()
            return HttpResponseRedirect(f'/verses')
    else:
        form = NewVerseForm()
    return render(request, "verses/new_story.html", {'form': form})



@login_required(login_url='/accounts/login')
def verse_list_view(request, *args, **kwargs):
    adjust_score(request, '/verses')
    nodes = Verse.objects.all().filter(parent=None).order_by('-vote_score')
    context = {'nodes': nodes}
    return render(request, "verses/list.html", context)

@login_required(login_url='/accounts/login')
def verse_reply_view(request, id):
    # adjust_score(request)
    this = Verse.objects.get(id=id)
    family = this.get_ancestors(include_self=True)
    if request.method == 'POST':
        form = VerseForm(request.POST)
        if form.is_valid():
            author = User.objects.get(id=request.user.id)
            genres = this.genre.all()
            story = request.POST['story']
            new_verse = Verse(body=story, parent=this, author=author)
            new_verse.save()
            new_verse.genre.set(genres)
            return HttpResponseRedirect(f'/verses/{id}')
    else:
        form = VerseForm()
    context = {'nodes': family, 'form': form, 'parent': id}
    return render(request, "verses/reply.html", context)

def verse_add_genre_view(request):
    if request.method == 'POST':
        form = AddGenreForm(request.POST)
        if form.is_valid():
            new_genre = Genre(name=request.POST['name'])
            new_genre.save()
            return HttpResponseRedirect(f'/verses/new')
    else:
        form = AddGenreForm()
    context = {'form': form}
    return render(request, "verses/add_genre.html", context)

def user_profile_view(request, username):
    me = User.objects.get(username=username)
    my_verses = Verse.objects.all().filter(author_id=me.id)
    my_voted = Verse.votes.all(me.id)

    num_written = len(my_verses)
    num_votes_given = len(my_voted)
    num_votes_received = sum(v.votes.count() for v in my_verses)

    # get favorite genre
    genres = []
    for v in my_voted:
        for g in v.genre.all():
            genres.append(g.name)
    genre_counts = Counter(genres)
    top_3_genres = list(zip(*genre_counts.most_common(3)))[0]

    # get favorite author
    authors = [v.author.username for v in my_voted]
    author_counts = Counter(authors)
    top_3_authors = list(zip(*author_counts.most_common(3)))[0]

    
    context ={'user': me, 'fav_authors': top_3_authors, 'fav_genres':top_3_genres, 'votes_given':num_votes_given,
            'votes_gotten': num_votes_received, 'num_written':num_written, 'verses': my_verses}
    return render(request, 'users/profile.html', context)
