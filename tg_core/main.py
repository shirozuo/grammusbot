import logging

from django.conf import settings
from django.utils import timezone
from telegram.ext import Application, ApplicationBuilder

from config.log_settings import format_log
from tg_core.handlers.start_handler import start_handler

token = settings.TG_BOT_TOKEN

log = logging.getLogger(__name__)


def get_app() -> Application:
    """Initialize and return a Telegram Application instance.

    Registers all handlers and prepares the bot for polling.
    """
    application = ApplicationBuilder().token(token).build()

    handlers = [
        start_handler,
    ]

    for handler in handlers:
        application.add_handler(handler)

    return application


if __name__ == "__main__":
    log.info(
        format_log(
            "polling_started", f"at {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
    )
    app = get_app()
    app.run_polling(drop_pending_updates=True)
