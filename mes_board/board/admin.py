from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Message, Author


class MessageAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post_link", "created_at", "comment")
    list_filter = ("user", "post")

    def post_link(self, obj):
        return mark_safe(
            f'<a href="{obj.post.get_absolute_url()}">{obj.post.title}</a>'
        )

    post_link.allow_tags = True


admin.site.register(Message, MessageAdmin)
admin.site.register(Author)