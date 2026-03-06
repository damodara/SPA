from urllib.parse import urlparse
from rest_framework.exceptions import ValidationError


def validate_youtube_url(value):
    """
    Валидатор для проверки, что переданная ссылка ведёт на YouTube.

    Проверяет, что URL соответствует одному из разрешённых форматов:
        - https://www.youtube.com/watch?v=...
        - https://youtube.com/watch?v=...
        - https://youtu.be/...

    Args:
        value (str): URL-ссылка, которую необходимо проверить.

    Returns:
        str: Возвращает исходное значение, если оно корректно.

    Raises:
        ValidationError: Если ссылка не ведёт на YouTube или имеет некорректный формат.
                         Также выбрасывается при попытке передать невалидный URL.

    Примеры допустимых ссылок:
        - "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        - "https://youtube.com/watch?v=dQw4w9WgXcQ"
        - "https://youtu.be/dQw4w9WgXcQ"

    Примеры недопустимых ссылок:
        - "https://example.com"
        - "https://youtube.com/evil_redirect?v=..."
        - "https://youtu.be/"

    Note:
        Пустые пути или отсутствующие идентификаторы видео считаются ошибкой.
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