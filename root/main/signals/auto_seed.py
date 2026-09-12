"""Auto-seed demo data right after ``python manage.py migrate``.

The ``seed`` management command already supports ``--if-empty`` (skip when
employees exist). This ``post_migrate`` receiver calls it automatically so a
fresh database is usable immediately after migration — including inside
Docker, where the entrypoint is just ``migrate``.

Guards (so migrate never breaks):
- opt-out with ``HR_AUTO_SEED=0`` / ``false`` / ``no``
- skipped while running tests (``test`` in ``sys.argv``)
- runs at most once per process (``post_migrate`` fires once per app)
- any seeding error is printed, never raised
"""
import os
import sys

from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.dispatch import receiver

_SEEDED_THIS_PROCESS = False


def _auto_seed_enabled():
    return os.environ.get('HR_AUTO_SEED', '1').lower() not in ('0', 'false', 'no', 'off')


def _running_tests():
    return 'test' in sys.argv or os.environ.get('PYTEST_RUNNING') == '1'


@receiver(post_migrate, dispatch_uid='main.auto_seed_after_migrate')
def seed_after_migrate(sender, **kwargs):
    global _SEEDED_THIS_PROCESS
    if _SEEDED_THIS_PROCESS:
        return
    if not _auto_seed_enabled() or _running_tests():
        return

    try:
        from core_module.models.employee.employee import Employee

        if Employee.objects.exists():
            _SEEDED_THIS_PROCESS = True
            return

        full = os.environ.get('HR_SEED_FULL', '1').lower() not in ('0', 'false', 'no', 'off')
        employees = int(os.environ.get('HR_SEED_EMPLOYEES', '50'))

        argv = f"seed --employees={employees} --if-empty{' --full' if full else ''}"
        print(f"[auto-seed] database empty -> running: manage.py {argv}", flush=True)
        call_command('seed', employees=employees, if_empty=True, full=full)
        _SEEDED_THIS_PROCESS = True
        print('[auto-seed] done.')
    except Exception as exc:  # noqa: BLE001 - migrate must never fail because of seeding
        # Most common benign cause: this app's post_migrate fired before all
        # tables exist (signal runs once per app); a later app's signal or the
        # next migrate run will seed successfully.
        print(f'[auto-seed] skipped ({type(exc).__name__}: {exc})')
