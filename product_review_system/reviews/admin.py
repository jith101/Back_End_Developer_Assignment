from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Product, Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'average_rating_display', 'review_count', 'created_by', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'average_rating_display', 'review_count')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price')
        }),
        (_('Metadata'), {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        (_('Statistics'), {
            'fields': ('average_rating_display', 'review_count'),
            'classes': ('collapse',)
        }),
    )
    
    def average_rating_display(self, obj):
        return f"{obj.average_rating:.1f} / 5.0"
    average_rating_display.short_description = _('Average Rating')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating_stars', 'created_at', 'updated_at')
    list_filter = ('rating', 'created_at', 'updated_at')
    search_fields = ('product__name', 'user__email', 'comment')
    readonly_fields = ('created_at', 'updated_at', 'rating_stars')
    fieldsets = (
        (None, {
            'fields': ('product', 'user', 'rating', 'rating_stars', 'comment')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def rating_stars(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    rating_stars.short_description = _('Rating')
    rating_stars.admin_order_field = 'rating'
