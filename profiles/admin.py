from django.contrib import admin

from profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for the Profile model."""

    list_display = (
        "id",
        "nickname",
        "tg_id",
    )
    list_filter = ("last_activity_dt",)
    search_fields = (
        "tg_id",
        "nickname",
        "first_name",
        "last_name",
    )
    ordering = ("-created_dt",)
    list_per_page = 50

    fields = (
        "user",
        "tg_id",
        "nickname",
        "first_name",
        "last_name",
        "created_dt",
        "modified_dt",
        "deleted_dt",
        "last_activity_dt",
    )

    readonly_fields = (
        "nickname",
        "created_dt",
        "modified_dt",
        "deleted_dt",
        "last_activity_dt",
    )
