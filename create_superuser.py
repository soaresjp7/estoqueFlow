import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque.settings')
django.setup()

from django.contrib.auth.models import User

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not password:
    print('DJANGO_SUPERUSER_PASSWORD nao definida — superusuario nao criado.')
else:
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.email = email
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f'Superusuario "{username}" criado com sucesso.')
    else:
        print(f'Superusuario "{username}" ja existe — nenhuma alteracao feita.')
