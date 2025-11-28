"""
This migration previously contained hardcoded plaintext passwords.
Hardcoding secrets in source control is unsafe for public repositories.

This version removes any plaintext passwords. It ensures an `admin` user
exists but creates/updates it with an unusable password so credentials
are never stored in the codebase. Administrators should set a real
password using Django's `changepassword` command or the admin UI.
"""

from django.db import migrations


def set_admin_password(apps, schema_editor):
    """Ensure an `admin` superuser exists with no usable password.

    This avoids storing plaintext passwords in migrations. After deployment,
    run `python manage.py changepassword admin` to set a proper password.
    """
    User = apps.get_model('auth', 'User')

    try:
        admin_user = User.objects.get(username='admin')
        admin_user.set_unusable_password()
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
    except User.DoesNotExist:
        # Create admin user with an unusable password; owner must set password later.
        admin_user = User.objects.create(
            username='admin',
            email='admin@example.com',
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        admin_user.set_unusable_password()
        admin_user.save()


def reverse_password_change(apps, schema_editor):
    # No reversible action: do nothing
    return


class Migration(migrations.Migration):

    dependencies = [
        ('People', '0013_student_absences'),
        ('auth', '__latest__'),
    ]

    operations = [
        migrations.RunPython(set_admin_password, reverse_code=reverse_password_change),
    ]
