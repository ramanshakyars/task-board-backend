from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "task", "user", "created_at"]
    list_filter = ["task"]
    search_fields = ["content", "user__username"]
