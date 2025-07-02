import logging
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any

from telegram import Update
from telegram.error import BadRequest, RetryAfter, TelegramError, TimedOut

from config.log_settings import format_log

log = logging.getLogger(__name__)


def _extract_telegram_context(*args, **kwargs) -> str:
    """Extract Telegram context from arguments.

    Returns a string with tg_id and message_id or chat_id for logging purposes.
    """
    for arg in args:
        if isinstance(arg, Update):
            tg_id = getattr(arg.effective_user, "id", "?")
            message_id = getattr(getattr(arg, "message", None), "id", "?")
            return f"tg_id='{tg_id}' message_id='{message_id}'"

    chat_id = kwargs.get("chat_id", "?")
    return f"tg_id='{chat_id}'"


def log_telegram_errors(
    action: str, context_extractor: Callable[..., str] = _extract_telegram_context
):
    """Wrap an async function and log Telegram-related errors.

    Adds identifying context to the log using the provided context extractor.
    """

    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except (BadRequest, TimedOut, RetryAfter, TelegramError, Exception) as e:
                context_info = context_extractor(*args, **kwargs)
                log.warning(format_log(action, f"{context_info} error='{e}'"))
                return None

        return wrapper

    return decorator
