from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Sets up default admin and normal users for the Task Board backend"

    def add_arguments(self, parser):
        parser.add_argument(
            "--admin-username",
            type=str,
            default="admin",
            help="Username for the admin user (default: admin)",
        )
        parser.add_argument(
            "--admin-password",
            type=str,
            default="admin123",
            help="Password for the admin user (default: admin123)",
        )
        parser.add_argument(
            "--admin-email",
            type=str,
            default="admin@example.com",
            help="Email for the admin user (default: admin@example.com)",
        )
        parser.add_argument(
            "--user-username",
            type=str,
            default="user",
            help="Username for the normal user (default: user)",
        )
        parser.add_argument(
            "--user-password",
            type=str,
            default="user123",
            help="Password for the normal user (default: user123)",
        )
        parser.add_argument(
            "--user-email",
            type=str,
            default="user@example.com",
            help="Email for the normal user (default: user@example.com)",
        )

    def handle(self, *args, **options):
        admin_username = options["admin_username"]
        admin_password = options["admin_password"]
        admin_email = options["admin_email"]

        user_username = options["user_username"]
        user_password = options["user_password"]
        user_email = options["user_email"]

        # 1. Setup Admin User
        admin_user, admin_created = User.objects.get_or_create(
            username=admin_username,
            defaults={"email": admin_email, "first_name": "Admin", "last_name": "User"},
        )
        admin_user.set_password(admin_password)
        admin_user.email = admin_email
        admin_user.first_name = "Admin"
        admin_user.last_name = "User"
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()

        if admin_created:
            self.stdout.write(self.style.SUCCESS(f"Successfully created admin user: '{admin_username}'"))
        else:
            self.stdout.write(self.style.WARNING(f"Updated existing admin user: '{admin_username}'"))

        # 2. Setup Normal User
        normal_user, user_created = User.objects.get_or_create(
            username=user_username,
            defaults={"email": user_email, "first_name": "Regular", "last_name": "User"},
        )
        normal_user.set_password(user_password)
        normal_user.email = user_email
        normal_user.first_name = "Regular"
        normal_user.last_name = "User"
        normal_user.is_staff = False
        normal_user.is_superuser = False
        normal_user.is_active = True
        normal_user.save()

        if user_created:
            self.stdout.write(self.style.SUCCESS(f"Successfully created normal user: '{user_username}'"))
        else:
            self.stdout.write(self.style.WARNING(f"Updated existing normal user: '{user_username}'"))

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("Users setup completed successfully!"))
        self.stdout.write("=" * 50)
        self.stdout.write(f"1. Admin User  -> Username: {admin_username} | Password: {admin_password} | Role: admin (staff & superuser)")
        self.stdout.write(f"2. Normal User -> Username: {user_username} | Password: {user_password} | Role: user (standard)")
        self.stdout.write("=" * 50 + "\n")
