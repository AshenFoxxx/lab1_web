from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from .caching import benchmark_home, get_benchmark, get_gallery_images, get_page
from .forms import FeedbackForm, GalleryImageForm, LoginForm, PageForm, RegisterForm
from .jobs import run_scheduled_jobs
from .models import DailyReminder, FeedbackMessage, GalleryImage, Page


def _page(page_type):
    return get_page(page_type)


def home(request):
    return render(request, 'club/home.html', {'page': _page(Page.HOME)})


def contacts(request):
    return render(request, 'club/contacts.html', {'page': _page(Page.CONTACTS)})


def gallery(request):
    form = GalleryImageForm() if request.user.is_authenticated else None
    return render(request, 'club/gallery.html', {
        'page': _page(Page.GALLERY),
        'images': get_gallery_images(),
        'form': form,
    })


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение отправлено. Мы свяжемся с вами в рабочее время.')
            return redirect('club:feedback')
    else:
        form = FeedbackForm()
    return render(request, 'club/feedback.html', {
        'page': _page(Page.FEEDBACK),
        'form': form,
    })


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    if page.page_type != Page.CUSTOM:
        return redirect(page.get_absolute_url())
    return render(request, 'club/page.html', {'page': page})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('club:home')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, f'Вы вошли как {request.user.username}.')
        return redirect(request.GET.get('next') or 'club:home')
    return render(request, 'club/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('club:home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Аккаунт создан. Теперь вы можете редактировать страницы.')
        return redirect('club:home')
    return render(request, 'club/register.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('club:home')


def _unique_slug(title, instance=None):
    base = slugify(title, allow_unicode=True) or 'page'
    slug = base
    index = 2
    while True:
        exists = Page.objects.filter(slug=slug)
        if instance:
            exists = exists.exclude(pk=instance.pk)
        if not exists.exists():
            return slug
        slug = f'{base}-{index}'
        index += 1


@login_required
def dashboard(request):
    return render(request, 'club/dashboard.html', {
        'pages_count': Page.objects.count(),
        'photos_count': GalleryImage.objects.count(),
        'messages_count': FeedbackMessage.objects.count(),
        'reminder': DailyReminder.objects.order_by('-day').first(),
        'benchmark': get_benchmark(),
    })


@login_required
@require_POST
def run_scheduler_view(request):
    reminder, deleted = run_scheduled_jobs()
    messages.success(
        request,
        f'{reminder.text} Удалено прочитанных заявок старше 30 дней: {deleted}.',
    )
    return redirect('club:dashboard')


@login_required
@require_POST
def benchmark_cache_view(request):
    result = benchmark_home()
    faster = ''
    if result['faster']:
        faster = f' С кэшем быстрее в {result["faster"]} раз.'
    messages.success(
        request,
        f'Без кэша: {result["cold_ms"]} мс. С кэшем: {result["warm_ms"]} мс '
        f'({result["repeats"]} сборок данных главной).{faster}',
    )
    return redirect('club:dashboard')


@login_required
def page_list(request):
    return render(request, 'club/page_list.html', {
        'pages': Page.objects.all(),
        'has_services': Page.objects.filter(slug='services').exists(),
    })


@login_required
@require_POST
def restore_services(request):
    from .seed import restore_page
    restore_page('services')
    messages.success(request, 'Страница «Услуги» восстановлена.')
    return redirect('club:page_list')


@login_required
def page_create(request):
    form = PageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        page = form.save(commit=False)
        page.page_type = Page.CUSTOM
        page.slug = _unique_slug(page.title)
        page.save()
        messages.success(request, 'Страница создана.')
        return redirect('club:page_list')
    return render(request, 'club/page_form.html', {
        'form': form,
        'form_title': 'Новая страница',
    })


@login_required
def page_edit(request, pk):
    page = get_object_or_404(Page, pk=pk)
    form = PageForm(request.POST or None, instance=page)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Страница сохранена.')
        return redirect(page.get_absolute_url())
    return render(request, 'club/page_form.html', {
        'form': form,
        'form_title': f'Редактирование: {page.title}',
        'page': page,
    })


@login_required
@require_POST
def page_delete(request, pk):
    page = get_object_or_404(Page, pk=pk)
    title = page.title
    page.delete()
    messages.success(request, f'Страница «{title}» удалена.')
    return redirect('club:page_list')


@login_required
def gallery_manage(request):
    form = GalleryImageForm()
    return render(request, 'club/gallery_manage.html', {
        'images': GalleryImage.objects.all(),
        'form': form,
    })


@login_required
@require_POST
def gallery_add(request):
    form = GalleryImageForm(request.POST, request.FILES)
    next_url = request.POST.get('next') or '/gallery/'
    if form.is_valid():
        form.save()
        messages.success(request, 'Фотография добавлена.')
    else:
        messages.error(request, 'Выберите файл изображения.')
    return redirect(next_url)


@login_required
@require_POST
def gallery_delete(request, pk):
    image = get_object_or_404(GalleryImage, pk=pk)
    if image.image:
        image.image.delete(save=False)
    image.delete()
    messages.success(request, 'Фотография удалена.')
    next_url = request.POST.get('next') or '/gallery/'
    return redirect(next_url)


@login_required
def feedback_list(request):
    return render(request, 'club/feedback_list.html', {
        'items': FeedbackMessage.objects.all(),
    })
