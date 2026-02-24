from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse
from .models import Producer


class ProductListViewTest(TestCase):
    def setUp(self):
        """
        Создание тестового пользователя и настройка прав доступа.
        Метод подготавливает зависимости (URL-пути, группы, учетные данные), необходимые
        для обеспечения изоляции и повторяемости каждого теста в классе.
        """
        self.url = reverse('manager')
        self.username = 'test'
        self.password = 'Test1234'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        manager_group, created = Group.objects.get_or_create(name='Менеджер')
        self.user.groups.add(manager_group)

    def test_model_creation(self):
        """
        Проверка корректности работы модели Producer.
        Тест верифицирует создание записи в базе данных и
        соответствие сохраненного атрибута 'name' ожидаемому значению.
        """
        obj = Producer.objects.create(name="Ситилинк")
        self.assertEqual(obj.name, "Ситилинк")

    def test_manager_login(self):
        """
        Интеграционная проверка механизма аутентификации и авторизации.
        Метод имитирует сессию пользователя и проверяет доступность
        защищенного URL-адреса для роли с соответствующими правами.
        """
        login_successful = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login_successful, "Логин не удался!")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_product_search(self):
        """
        Тестирование фильтрации данных через GET-запрос.
        Проверяет работу контроллера при обработке параметров
        строки запроса и корректность отображения отфильтрованного контента.
        """
        self.client.login(username=self.username, password=self.password)
        producer_url = f"{self.url}?q=1"
        response = self.client.get(producer_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1")
