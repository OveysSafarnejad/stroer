import os
from pathlib import Path

import dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv.read_dotenv(BASE_DIR.parent.parent / ".env")

PROFILE = os.environ.get("PROFILE")

match PROFILE:
    case 'test':
        from stroer.settings.test import *  # noqa
    case 'development':
        from stroer.settings.development import *  # noqa
    case 'production':
        from stroer.settings.production import *  # noqa
    case _:
        raise SystemExit(
            f'Invalid environment variable {PROFILE}'
        )
