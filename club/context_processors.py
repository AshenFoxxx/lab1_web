from .models import Page


def menu_pages(request):
    return {
        'menu_pages': Page.objects.filter(show_in_menu=True),
    }
