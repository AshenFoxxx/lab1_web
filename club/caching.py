import time
from contextlib import contextmanager
from contextvars import ContextVar

from django.core.cache import cache

from .models import GalleryImage, Page

TIMEOUT = 120
MENU_KEY = 'club:menu-pages'
GALLERY_KEY = 'club:gallery-images'
CATALOG_KEY = 'club:public-catalog'
BENCHMARK_KEY = 'club:benchmark'
_MISSING = object()
_bypass = ContextVar('mayak_cache_bypass', default=False)


def _page_key(page_type):
    return f'club:page:{page_type}'


@contextmanager
def without_cache():
    token = _bypass.set(True)
    try:
        yield
    finally:
        _bypass.reset(token)


def invalidate_public_cache():
    keys = [MENU_KEY, GALLERY_KEY, CATALOG_KEY]
    keys.extend(_page_key(value) for value, _label in Page.PAGE_TYPES)
    cache.delete_many(keys)


def get_menu_pages():
    if _bypass.get():
        return list(Page.objects.filter(show_in_menu=True))
    pages = cache.get(MENU_KEY, _MISSING)
    if pages is _MISSING:
        pages = list(Page.objects.filter(show_in_menu=True))
        cache.set(MENU_KEY, pages, TIMEOUT)
    return pages


def get_page(page_type):
    if _bypass.get():
        return Page.objects.filter(page_type=page_type).first()
    key = _page_key(page_type)
    page = cache.get(key, _MISSING)
    if page is _MISSING:
        page = Page.objects.filter(page_type=page_type).first()
        cache.set(key, page if page is not None else False, TIMEOUT)
    if page is False:
        return None
    return page


def get_gallery_images():
    if _bypass.get():
        return list(GalleryImage.objects.all())
    images = cache.get(GALLERY_KEY, _MISSING)
    if images is _MISSING:
        images = list(GalleryImage.objects.all())
        cache.set(GALLERY_KEY, images, TIMEOUT)
    return images


def get_public_catalog():
    if _bypass.get():
        return _build_catalog()
    catalog = cache.get(CATALOG_KEY, _MISSING)
    if catalog is _MISSING:
        catalog = _build_catalog()
        cache.set(CATALOG_KEY, catalog, TIMEOUT)
    return catalog


def _build_catalog():
    return {
        'pages': list(
            Page.objects.order_by('menu_order', 'id').values_list('title', flat=True)
        ),
        'photos': GalleryImage.objects.count(),
    }


def load_home_data():
    """Данные, которые главная страница берёт из базы или из кэша."""
    return {
        'page': get_page(Page.HOME),
        'menu': get_menu_pages(),
        'catalog': get_public_catalog(),
    }


def get_benchmark():
    return cache.get(BENCHMARK_KEY)


def benchmark_home(repeats=50):
    """Сравнивает время сборки данных главной без кэша и с кэшем."""
    with without_cache():
        started = time.perf_counter()
        for _ in range(repeats):
            load_home_data()
        cold_ms = (time.perf_counter() - started) * 1000

    load_home_data()
    started = time.perf_counter()
    for _ in range(repeats):
        load_home_data()
    warm_ms = (time.perf_counter() - started) * 1000

    result = {
        'cold_ms': round(cold_ms, 2),
        'warm_ms': round(warm_ms, 2),
        'repeats': repeats,
        'faster': round(cold_ms / warm_ms, 1) if warm_ms > 0 else None,
    }
    cache.set(BENCHMARK_KEY, result, 60 * 60 * 24)
    return result
