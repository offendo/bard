from django.shortcuts import render
from .models import Verse

# Create your views here.
def story_view(request):
    queryset = Verse.objects.get(id=request.id)
    context = {"object": queryset}
    return render(request, "verses/story.html", context)


def story_list_view(request, *args, **kwargs):
    queryset = Verse.objects.all()
    context = {"object_list": queryset}
    return render(request, "verses/list.html", context)
