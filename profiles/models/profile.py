from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    """Profile model representing a Telegram user linked to a Django user.

    Includes timestamps for creation, updates, blocking, deletion, and activity.
    Also stores Telegram-specific data such as tg_id and username.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Linked Django user (optional).",
    )
    nickname = models.CharField(
        max_length=256,
        editable=False,
        help_text="Telegram username (without @).",
    )
    first_name = models.CharField(
        max_length=256,
        default="",
        blank=True,
        help_text="First name.",
    )
    last_name = models.CharField(
        max_length=256,
        default="",
        blank=True,
        help_text="Last name.",
    )
    tg_id = models.CharField(
        max_length=256,
        unique=True,
        default="",
        blank=False,
        help_text="Unique Telegram user ID as a string.",
    )
    created_dt = models.DateTimeField(
        editable=False,
        help_text="Profile creation timestamp.",
    )
    modified_dt = models.DateTimeField(
        editable=False,
        help_text="Last modification timestamp.",
    )
    blocked_dt = models.DateTimeField(
        editable=False,
        null=True,
        help_text="Timestamp of blocking (if blocked).",
    )
    deleted_dt = models.DateTimeField(
        editable=True,
        blank=True,
        null=True,
        help_text="Soft delete timestamp (if deleted).",
    )
    last_activity_dt = models.DateTimeField(
        editable=False,
        null=True,
        help_text="Timestamp of last user activity.",
    )

    def save(self, *args, **kwargs) -> None:
        """Save the profile with updated timestamps."""
        if not self.pk:
            self.created_dt = timezone.now()
        self.modified_dt = timezone.now()
        return super().save(*args, **kwargs)

    async def asave(self, *args, **kwargs) -> None:
        """Asynchronously save the profile with updated timestamps."""
        if not self.pk:
            self.created_dt = timezone.now()
        self.modified_dt = timezone.now()
        return await super().asave(*args, **kwargs)

    async def block(self) -> None:
        """Mark the profile as blocked with the current timestamp."""
        self.blocked_dt = timezone.now()
        await self.asave()

    def is_deleted(self) -> bool:
        """Return True if the profile is marked as deleted."""
        return self.deleted_dt is not None

    def get_full_name(self) -> str:
        """Return the full name of the user (first + last name)."""
        return f"{self.first_name} {self.last_name}".strip()

    def update_activity(self) -> None:
        """Update the timestamp of the last user activity."""
        self.last_activity_dt = timezone.now()
        self.save(update_fields=["last_activity_dt"])

    def __str__(self) -> str:
        """Return a string representation of the profile."""
        return f"{self.pk} {self.nickname}"

    class Meta:
        """Meta options for the Profile model."""

        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["-created_dt"]
        indexes = [
            models.Index(fields=["created_dt"]),
        ]
