from django.contrib import admin
from .models import Review, Assignment

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewee', 'rating', 'created_at')
    search_fields = ('reviewer__username', 'reviewee__username')
    list_filter = ('rating', 'created_at')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'created_at')
    search_fields = ('title',)
    list_filter = ('due_date',)
