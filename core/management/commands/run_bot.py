import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from telegram.ext import Application

from config.log_settings import format_log
from tg_core.main import get_app

log = logging.getLogger(__name__)
token = settings.TG_BOT_TOKEN


class Command(BaseCommand):
    """Custom Django management command to start the Telegram bot."""

    help = "Start Telegram bot"
    app: Application = None

    def handle(self, *args, **options):
        """Handle the execution of the command."""
        now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        log.info(format_log("polling_started", f"at {now}"))
        self.stdout.write(self.style.SUCCESS(f"Polling started at {now}"))

        self.app = get_app()

        self.app.run_polling(drop_pending_updates=True)

        now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        log.info(format_log("polling_stopped", f"at {now}"))
        self.stdout.write(self.style.SUCCESS(f"Polling stopped at {now}"))
