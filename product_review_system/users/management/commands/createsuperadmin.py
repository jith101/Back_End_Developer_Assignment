from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser with admin role'

    def handle(self, *args, **options):
        email = input('Email: ')
        first_name = input('First name: ')
        last_name = input('Last name: ')
        password = input('Password: ')
        confirm_password = input('Confirm Password: ')

        if password != confirm_password:
            self.stderr.write("Error: Passwords don't match")
            return

        if not email:
            self.stderr.write('Error: Email cannot be empty')
            return

        if not first_name:
            self.stderr.write('Error: First name cannot be empty')
            return

        if not last_name:
            self.stderr.write('Error: Last name cannot be empty')
            return

        if User.objects.filter(email=email).exists():
            self.stderr.write('Error: User with this email already exists')
            return

        try:
            user = User.objects.create_superuser(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {email}'))
        except Exception as e:
            self.stderr.write(f'Error creating user: {str(e)}')
