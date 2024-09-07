from django.contrib import admin
from main.models import Slide, Theme, Presentation

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('index', 'html')
    list_editable = ('html',)
    ordering = ('index',)

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_title')
    list_display_links = ('name',)
    search_fields = ('name',)

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_display_links = ('name',)
    search_fields = ('name',)


