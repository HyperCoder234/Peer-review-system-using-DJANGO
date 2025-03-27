from django.conf import settings
from pathlib import Path

# 📂 Define Upload Paths for Assignments & Reviews
ASSIGNMENT_UPLOAD_PATH = Path(settings.MEDIA_ROOT) / "assignments/"
REVIEW_UPLOAD_PATH = Path(settings.MEDIA_ROOT) / "reviews/"

# 📂 Ensure Directories Exist
ASSIGNMENT_UPLOAD_PATH.mkdir(parents=True, exist_ok=True)
REVIEW_UPLOAD_PATH.mkdir(parents=True, exist_ok=True)
