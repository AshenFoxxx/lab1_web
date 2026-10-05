from django.urls import path

from . import views

app_name = 'club'

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('gallery/', views.gallery, name='gallery'),
    path('feedback/', views.feedback, name='feedback'),
    path('p/<slug:slug>/', views.page_detail, name='page_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('manage/', views.dashboard, name='dashboard'),
    path('manage/scheduler/run/', views.run_scheduler_view, name='run_scheduler'),
    path('manage/cache/benchmark/', views.benchmark_cache_view, name='benchmark_cache'),
    path('manage/pages/', views.page_list, name='page_list'),
    path('manage/pages/restore-services/', views.restore_services, name='restore_services'),
    path('manage/gallery/', views.gallery_manage, name='gallery_manage'),
    path('manage/pages/new/', views.page_create, name='page_create'),
    path('manage/pages/<int:pk>/edit/', views.page_edit, name='page_edit'),
    path('manage/pages/<int:pk>/delete/', views.page_delete, name='page_delete'),
    path('manage/gallery/add/', views.gallery_add, name='gallery_add'),
    path('manage/gallery/<int:pk>/delete/', views.gallery_delete, name='gallery_delete'),
    path('manage/messages/', views.feedback_list, name='feedback_list'),
]
