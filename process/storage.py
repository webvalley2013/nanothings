from django.core.files.storage import FileSystemStorage
from nanothings.settings import DEFAULT_INPUT_PATH

tmpfs= FileSystemStorage(location=DEFAULT_INPUT_PATH)
