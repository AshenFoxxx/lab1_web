from django.contrib.auth.models import User

from .models import FeedbackMessage, GalleryImage, Page


SERVICES_HTML = """
<p>Принимаем электропневматику (AEG), GBB, HPA и пистолеты. Перед работой делаем дефектовку: разбираем, смотрим износ шестерней, поршня, направляющей пружины и проводки. Запчасти клиента ставим по согласованию.</p>
<table class="data-table">
  <thead>
    <tr>
      <th>Услуга</th>
      <th>Срок</th>
      <th>Что входит</th>
      <th>Цена</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Диагностика / дефектовка</td><td>1 день</td><td>Разбор, заключение, смета</td><td>1 000 ₽*</td></tr>
    <tr><td>Полное ТО привода</td><td>3–5 дней</td><td>Чистка, смазка, шиммовка, AOE, компрессия</td><td>от 3 500 ₽</td></tr>
    <tr><td>Переборка гирбокса V2 / V3</td><td>5–7 дней</td><td>Шестерни, поршень, голова, антиреверс</td><td>от 5 500 ₽</td></tr>
    <tr><td>Гирбокс DSG / high-speed</td><td>7–10 дней</td><td>Сборка под короткое касание, мотор, пружина</td><td>от 12 000 ₽</td></tr>
    <tr><td>Замена пружины / настройка FPS</td><td>2–3 дня</td><td>Пружина, направляющая, замер на хроно</td><td>от 1 800 ₽</td></tr>
    <tr><td>Мотор, шестерни, поршень</td><td>2–4 дня</td><td>Подбор под ваш гирбокс и стиль стрельбы</td><td>от 1 500 ₽ + деталь</td></tr>
    <tr><td>Хоп-ап: камера, резинка, нубук</td><td>1–2 дня</td><td>Герметизация, подгонка, тест дальности</td><td>от 2 000 ₽</td></tr>
    <tr><td>Стволик 6.03 / 6.01</td><td>1–2 дня</td><td>Установка, центровка камеры</td><td>от 1 500 ₽</td></tr>
    <tr><td>MOSFET и проводка</td><td>3–4 дня</td><td>Пайка, предохранитель, разъём Deans/XT60</td><td>от 4 500 ₽</td></tr>
    <tr><td>Ремонт магазина / фурнитуры</td><td>1–3 дня</td><td>Горло, пружина, крышка, приклад, цевьё</td><td>от 800 ₽</td></tr>
    <tr><td>Сборка кастома под ключ</td><td>по проекту</td><td>Конфиг, закуп, сборка, отстрел</td><td>от 15 000 ₽</td></tr>
  </tbody>
</table>
<p>* Стоимость диагностики идёт в зачёт ремонта, если оставляете привод у нас.</p>
"""

PAGES = [
    {
        'title': 'Главная',
        'slug': 'home',
        'page_type': Page.HOME,
        'subtitle': 'ТО приводов, гирбоксы и комплектующие',
        'content': 'Маяк — мастерская, где чинят и собирают страйкбольные приводы: от планового ТО до кастомного гирбокса.',
        'menu_order': 1,
        'is_system': True,
    },
    {
        'title': 'Контакты',
        'slug': 'contacts',
        'page_type': Page.CONTACTS,
        'subtitle': 'Сдать привод на ТО или забрать после ремонта',
        'content': """
<p>Привоз лучше согласовать в мессенджере: скажем, когда мастер свободен и какие запчасти лучше взять с собой.</p>
<table class="data-table">
  <thead>
    <tr><th>День</th><th>Приём приводов</th><th>Мастер за верстаком</th></tr>
  </thead>
  <tbody>
    <tr><td>Понедельник — пятница</td><td>11:00–21:00</td><td>12:00–20:30</td></tr>
    <tr><td>Суббота</td><td>12:00–20:00</td><td>12:00–19:30</td></tr>
    <tr><td>Воскресенье</td><td>выходной</td><td>только срочный ремонт по записи</td></tr>
  </tbody>
</table>
<ul class="info-list">
  <li><strong>Адрес:</strong> Обнинск, проспект Маркса, 83</li>
  <li><strong>Телефон:</strong> +7 (960) 514-88-52</li>
  <li><strong>Email:</strong> mayakairsft@gmail.com</li>
  <li><strong>Ориентир:</strong> 55-й микрорайон</li>
</ul>
""",
        'menu_order': 2,
        'is_system': True,
    },
    {
        'title': 'Наши работы',
        'slug': 'gallery',
        'page_type': Page.GALLERY,
        'subtitle': '',
        'content': '',
        'menu_order': 3,
        'is_system': True,
    },
    {
        'title': 'Заявка на ТО',
        'slug': 'feedback',
        'page_type': Page.FEEDBACK,
        'subtitle': 'Опишите модель привода и что с ним не так',
        'content': 'Напишите модель, симптомы (не крутит, режет шестерни, слабый хоп, греется мотор) и желаемые сроки. Мастер ответит в рабочий день.',
        'menu_order': 4,
        'is_system': True,
    },
    {
        'title': 'Услуги',
        'slug': 'services',
        'page_type': Page.CUSTOM,
        'subtitle': 'Прайс на ТО, гирбоксы и замену комплектующих',
        'content': SERVICES_HTML,
        'menu_order': 5,
        'is_system': False,
    },
]

GALLERY = [
    ('', '', '/static/img/gallery/01.jpg'),
    ('', '', '/static/img/gallery/02.jpg'),
    ('', '', '/static/img/gallery/03.jpg'),
]


def ensure_users():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@mayak.shop', 'admin123')
    if not User.objects.filter(username='manager').exists():
        User.objects.create_user('manager', 'manager@mayak.shop', 'manager123')


def seed_if_empty():
    ensure_users()
    if not Page.objects.exists():
        for data in PAGES:
            Page.objects.create(**data, show_in_menu=True)
    if not GalleryImage.objects.exists():
        GalleryImage.objects.bulk_create([
            GalleryImage(title=title, description=desc, image_url=url)
            for title, desc, url in GALLERY
        ])
    if not FeedbackMessage.objects.exists():
        FeedbackMessage.objects.create(
            name='Илья Сорокин',
            email='ilya@example.com',
            phone='+7 900 111-22-33',
            message='AK CYMA, после игры режет шестерни. Нужно ТО гирбокса и замена поршня.',
        )


def restore_page(slug):
    data = next((item for item in PAGES if item['slug'] == slug), None)
    if not data:
        return None
    page, _ = Page.objects.update_or_create(
        slug=data['slug'],
        defaults={
            'title': data['title'],
            'page_type': data['page_type'],
            'subtitle': data['subtitle'],
            'content': data['content'],
            'show_in_menu': True,
            'menu_order': data['menu_order'],
            'is_system': data['is_system'],
        },
    )
    return page


def refresh_demo_content():
    ensure_users()
    Page.objects.filter(slug='memberships').update(slug='services')
    for data in PAGES:
        Page.objects.update_or_create(
            slug=data['slug'],
            defaults={
                'title': data['title'],
                'page_type': data['page_type'],
                'subtitle': data['subtitle'],
                'content': data['content'],
                'show_in_menu': True,
                'menu_order': data['menu_order'],
                'is_system': data['is_system'],
            },
        )
    GalleryImage.objects.all().delete()
    GalleryImage.objects.bulk_create([
        GalleryImage(title=title, description=desc, image_url=url)
        for title, desc, url in GALLERY
    ])
    if not FeedbackMessage.objects.filter(email='ilya@example.com').exists():
        FeedbackMessage.objects.create(
            name='Илья Сорокин',
            email='ilya@example.com',
            phone='+7 900 111-22-33',
            message='AK CYMA, после игры режет шестерни. Нужно ТО гирбокса и замена поршня.',
        )
