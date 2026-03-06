from rest_framework.pagination import PageNumberPagination


class CourseLessonPagination(PageNumberPagination):
    """
    Пагинатор для курсов и уроков.
    Позволяет контролировать количество элементов на странице.
    """

    page_size = 10  # Количество элементов на одной странице
    page_size_query_param = "page_size"  # Позволяет клиенту указать размер страницы
    max_page_size = 100  # Максимальное количество элементов на странице
