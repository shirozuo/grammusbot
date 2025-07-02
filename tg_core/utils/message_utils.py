import logging

import telegram
from django.conf import settings
from telegram import Message, Update

from tg_core.utils.decorators import log_telegram_errors

log = logging.getLogger(__name__)
_bot = telegram.Bot(settings.TG_BOT_TOKEN)


def get_bot() -> telegram.Bot:
    """Return a singleton instance of the Telegram bot."""
    return _bot


@log_telegram_errors("send_failed")
async def send_message(*args, **kwargs) -> Message | None:
    """Send a message using the Telegram bot with error logging."""
    bot = get_bot()

    return await bot.send_message(*args, **kwargs)


@log_telegram_errors("edit_failed")
async def edit_message(*args, **kwargs) -> Message | None:
    """Edit a message using the Telegram bot with error logging."""
    bot = get_bot()

    return await bot.edit_message_text(*args, **kwargs)


async def _delete_message(*args, **kwargs) -> None:
    """Delete a message using the Telegram bot."""
    bot = get_bot()

    await bot.delete_message(*args, **kwargs)


@log_telegram_errors("delete_failed")
async def safe_delete_user_message(update: Update) -> None:
    """Safely delete a user's message if it exists in the update object."""
    if not update.message:
        return
    await _delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.message.id,
    )
