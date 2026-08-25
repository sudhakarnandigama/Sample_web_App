"""Application configuration read from environment variables.

See docs/wiki/ops/env-vars.md for the canonical variable list.
"""

import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./training_demo.db")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:4200")

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET is not configured. Export JWT_SECRET before starting the backend.")
