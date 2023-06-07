from .models import category

def menu_links(request):
    links = category.objects.all()
    return dict(links=links)