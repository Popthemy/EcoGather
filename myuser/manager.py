from django.contrib.auth.models import BaseUserManager


class CustomBaseUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        '''create and save user with the given details'''

        if not email:
            raise ValueError({'email': 'email is a required field'})

        email = self.normalize_email(email)
        user = self.model(

            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be True')

        if not email:
            raise ValueError({'email': 'valid email must be provided'})

        email = self.normalize_email(email)

        super_user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )

        super_user.save()
        return super_user
