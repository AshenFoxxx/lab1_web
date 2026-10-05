from django.db import models
from django.urls import reverse


class Page(models.Model):
    HOME = 'home'
    CONTACTS = 'contacts'
    GALLERY = 'gallery'
    FEEDBACK = 'feedback'
    CUSTOM = 'custom'

    PAGE_TYPES = [
        (HOME, 'Главная'),
        (CONTACTS, 'Контакты'),
        (GALLERY, 'Наши работы'),
        (FEEDBACK, 'Обратная связь'),
        (CUSTOM, 'Произвольная'),
    ]

    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('ЧПУ (slug)', unique=True)
    page_type = models.CharField(
        'Тип страницы', max_length=20, choices=PAGE_TYPES, default=CUSTOM
    )
    subtitle = models.CharField('Подзаголовок', max_length=400, blank=True)
    content = models.TextField('Содержимое (HTML)', blank=True)
    show_in_menu = models.BooleanField('Показывать в меню', default=True)
    menu_order = models.PositiveIntegerField('Порядок в меню', default=0)
    is_system = models.BooleanField('Системная страница', default=False)
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        ordering = ['menu_order', 'id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        routes = {
            self.HOME: 'club:home',
            self.CONTACTS: 'club:contacts',
            self.GALLERY: 'club:gallery',
            self.FEEDBACK: 'club:feedback',
        }
        if self.page_type in routes:
            return reverse(routes[self.page_type])
        return reverse('club:page_detail', kwargs={'slug': self.slug})


class GalleryImage(models.Model):
    title = models.CharField('Название', max_length=200, blank=True)
    description = models.CharField('Описание', max_length=400, blank=True)
    image = models.ImageField('Файл', upload_to='gallery/', blank=True)
    image_url = models.CharField('Ссылка на изображение', max_length=500, blank=True)
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Наши работы'
        ordering = ['id']

    def __str__(self):
        return self.title or f'Фото {self.pk}'

    @property
    def src(self):
        if self.image:
            return self.image.url
        return self.image_url


class DailyReminder(models.Model):
    day = models.DateField('День', unique=True)
    text = models.CharField('Текст', max_length=400)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Напоминание'
        verbose_name_plural = 'Напоминания планировщика'
        ordering = ['-day']

    def __str__(self):
        return self.text


class FeedbackMessage(models.Model):
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=30, blank=True)
    message = models.TextField('Сообщение')
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField('Отправлено', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name}: {self.message[:40]}'
