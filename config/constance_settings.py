from pathlib import Path

CONSTANCE_CONFIG = {
    "LOG_FILE": (
        str(Path(__file__).resolve().parent.parent / "logs" / "app.log"),
        "Log file path.",
    ),
}

CONSTANCE_CONFIG_FIELDSETS = {
    "Logging": ("LOG_FILE",),
}
