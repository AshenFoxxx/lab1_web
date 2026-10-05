from .caching import get_menu_pages


def menu_pages(request):
    return {
        'menu_pages': get_menu_pages(),
    }
