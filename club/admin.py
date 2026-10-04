from django.contrib import admin

from .models import FeedbackMessage, GalleryImage, Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'page_type', 'show_in_menu', 'menu_order', 'is_system')
    list_filter = ('page_type', 'show_in_menu', 'is_system')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug')


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(FeedbackMessage)
class FeedbackMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_read', 'created_at')
    list_filter = ('is_read',)
