import os
from pathlib import Path

PORT = int(os.getenv("PORT", 8007))
print(PORT)

CACHE_AGE = 60 * 60 * 24

PROJECT_DIR = Path(__file__).parent.resolve()