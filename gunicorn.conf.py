"""Gunicorn loads this file automatically from the project root.

Safety net for Render: applies database migrations (and creates the admin user
from DJANGO_SUPERUSER_* env vars) every time the server starts, so the site
works even if the service's Build Command doesn't run build.sh. Both steps are
idempotent.
"""
import os


def on_starting(server):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    import django

    django.setup()

    from django.core.management import call_command
    from django.db import connections

    try:
        call_command("migrate", interactive=False)
        call_command("ensure_superuser")
    except Exception:
        server.log.exception("Startup migrate/ensure_superuser failed")
    finally:
        connections.close_all()  # don't share DB connections with workers
