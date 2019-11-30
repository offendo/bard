from django.shortcuts import render
from .models import Verse

# Create your views here.
def verse_detail_view(request, id):
    this = Verse.objects.get(id=id)
    root = Verse.objects.all().filter(tree_id=this.tree_id)
    context = {'nodes': root}
    return render(request, "verses/verse.html", context)


def verse_list_view(request, *args, **kwargs):
    queryset = Verse.objects.all().filter(parent=None)
    context = {"object_list": queryset}
    return render(request, "verses/list.html", context)
