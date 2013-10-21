try:
    from django.db.transaction import atomic
    rollback = lambda: None
except ImportError:
    from django.db.transaction import commit_on_success as atomic, rollback  # noqa
