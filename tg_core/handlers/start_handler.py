import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config.log_settings import format_log
from tg_core.utils.message_utils import safe_delete_user_message, send_message
from tg_core.utils.profile_utils import get_or_create_profile

log = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command from the user.

    Deletes the user's message, retrieves or creates their profile,
    and sends a welcome message.
    """
    log.info(format_log("start_command", f'tg_id="{update.effective_user.id}"'))

    await safe_delete_user_message(update)

    profile = await get_or_create_profile(update)

    start_message = "Start message!"

    await send_message(
        chat_id=profile.tg_id,
        text=start_message,
    )


start_handler = CommandHandler("start", start)
