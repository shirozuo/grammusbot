@echo off
SET CMD=%1

IF "%CMD%"=="run" (
    python manage.py runserver
) ELSE IF "%CMD%"=="run_bot" (
    python manage.py run_bot
) ELSE IF "%CMD%"=="test" (
    pytest -v
) ELSE IF "%CMD%"=="lint" (
    ruff check .
) ELSE IF "%CMD%"=="format" (
    ruff format .
) ELSE IF "%CMD%"=="migrations" (
    python manage.py makemigrations
) ELSE IF "%CMD%"=="migrate" (
    python manage.py migrate
) ELSE IF "%CMD%"=="superuser" (
    python manage.py createsuperuser
) ELSE IF "%CMD%"=="shell" (
    python manage.py shell
) ELSE IF "%CMD%"=="check" (
    python manage.py check
) ELSE IF "%CMD%"=="setup" (
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py check
    pre-commit install
    echo Setup completed!
) ELSE (
    echo Unknown command: %CMD%
    echo Available commands: run, run_bot, test, lint, format, migrations, migrate, superuser, shell, check, setup
)
