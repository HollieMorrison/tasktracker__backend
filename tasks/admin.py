from django.contrib import admin

# Register your models here.
from .models import Task, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "state", "due_date", "is_overdue", "created_by", "created_at")
    list_filter = ("priority", "state", "category", "is_overdue", "created_at", "due_date")
    search_fields = ("title", "description")
    autocomplete_fields = ("created_by", "owners", "category")
    filter_horizontal = ("owners",)  # Better UI for ManyToMany
    date_hierarchy = "due_date"
    ordering = ("-created_at",)