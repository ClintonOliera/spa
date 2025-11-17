import os
from django.contrib.auth import get_user_model
from django.db import OperationalError, ProgrammingError

def create_admin_user(sender, **kwargs):
    """
    Create a superuser after migrations run (only once).
    """
    if os.environ.get("CREATE_SUPERUSER") != "yes":
        return

    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "Admin")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "adminlavylotus@gmail.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "KenyaKwanza")

    User = get_user_model()
    try:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print("Superuser created by post_migrate signal.")
    except (OperationalError, ProgrammingError) as e:
        # DB might not be ready yet in some edge cases — log and ignore
        print("Could not create superuser yet:", e)