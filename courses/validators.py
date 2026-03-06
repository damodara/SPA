from urllib.parse import urlparse
from rest_framework.exceptions import ValidationError

def validate_youtube_url(value):
    """
    Валидатор для проверки, что ссылка ведёт только на YouTube.
    Разрешены форматы: https://www.youtube.com/watch?v=... или https://youtu.be/...
    """
    try:
        parsed_url = urlparse(value)

        # Проверяем hostname
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com', 'youtu.be']:
            if parsed_url.hostname == 'www.youtube.com' and parsed_url.path == '/watch':
                if parsed_url.query.startswith('v='):
                    return value
            elif parsed_url.hostname == 'youtube.com' and parsed_url.path == '/watch':
                if parsed_url.query.startswith('v='):
                    return value
            elif parsed_url.hostname == 'youtu.be':
                if parsed_url.path[1:]:  # проверка, что после / есть идентификатор
                    return value

        raise ValidationError(f"Ссылки разрешены только на YouTube (youtube.com или youtu.be), получено: {value}")

    except Exception as e:
        raise ValidationError(f"Некорректный URL: {value}")