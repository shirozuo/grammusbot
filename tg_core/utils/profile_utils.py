import logging

from django.core.exceptions import ObjectDoesNotExist
from telegram import Update

from config.log_settings import format_log
from profiles.models import Profile

log = logging.getLogger(__name__)


async def get_or_create_profile(update: Update) -> Profile:
    """Get an existing profile by Telegram ID or create a new one.

    If the profile was previously marked as deleted, reset the deletion state.
    """
    try:
        profile: Profile = await Profile.objects.aget(tg_id=update.effective_user.id)
    except ObjectDoesNotExist:
        profile = await _initialize_new_user(update)

    if profile.is_deleted():
        profile.deleted_dt = None
        await profile.asave()
        log.info(format_log("profile_restarted", f"tg_id='{update.effective_user.id}'"))

    return profile


async def _initialize_new_user(update: Update) -> Profile:
    """Create and return a new profile based on Telegram user data.

    Log creation event if the profile is newly created.
    """
    profile, created = await Profile.objects.aget_or_create(
        tg_id=update.effective_user.id,
        defaults={
            "nickname": update.effective_user.name or "",
            "first_name": update.effective_user.first_name or "",
            "last_name": update.effective_user.last_name or "",
        },
    )

    if created:
        log.info(format_log("profile_created", f"tg_id='{update.effective_user.id}'"))

    return profile
