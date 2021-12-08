#!/usr/bin/env python
import os
import sys
from pathlib import Path

DEBUG = os.environ.get('DEBUG')

if __name__ == "__main__":
    if eval(DEBUG) == True:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "sayches"))

    execute_from_command_line(sys.argv)
