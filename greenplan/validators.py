from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size = 4

    if file.size > max_size * 1024* 1024:
        raise ValidationError(
            f'Image size must not be greater than {max_size}mb!')
