from django.test import TestCase, RequestFactory

from django.contrib.auth.models import User
from django.urls import reverse
from .views import *


class LRTestCases(TestCase):

    # -------- LOGIN/REG TESTS-----------

    def setUp(self) -> None:
        self.register_url = reverse('registration')
        self.login_url = reverse('login')
        Tags.objects.create(tg_name="тест")
        return super().setUp()

    def test_reg_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainP/registration.html')
        self.assertEqual(type(response.context['form']), CreateUserForm)

    def test_log_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainP/login.html')

    def test_can_reg(self):
        response = self.client.post(self.register_url, data={'username': 'testingUser',
                                                             'password': '11111aaaaa',
                                                             'email': 'test-e@mail.ru',
                                                             'first_name': 'Имя',
                                                             'last_name': 'Фамилия'})
        self.assertEqual(response.status_code, 200)

    def test_can_log(self):
        url = reverse('login')
        self.client.login(username='test', password='11111aaaaa')
        response = self.client.post(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_cant_log(self):
        url = reverse('login')
        self.client.login(username='a', password='11111')
        response = self.client.post(reverse('login'))
        self.assertEqual(response.status_code, 200)

    # -------- LOAD PAGE&FORMS TESTS-----------

    def test_creation_home_page_get(self):
        url = reverse('home')
        response = self.client.get(url)
        # print(response)

    def test_creation_proj_page_get(self):
        url = reverse('projects')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # print(response)


class TestViewsCases(TestCase):
    def setUp(self) -> None:
        self.register_url = reverse('registration')
        self.login_url = reverse('login')
        self.index = reverse('start')
        self.home = reverse('home')
        self.projects = reverse('projects')

        return super().setUp()

    # def test_proj(self):







