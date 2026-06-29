from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Division


class DivisionViewTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='division-admin',
            password='test-password',
            is_staff=True,
        )
        self.client.force_login(self.admin)

    def test_division_list_renders(self):
        response = self.client.get(reverse('users:division_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/division_list.html')

    def test_division_create_form_renders(self):
        response = self.client.get(reverse('users:division_add'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/division_form.html')

    def test_division_update_form_renders(self):
        division = Division.objects.create(name='Information Technology')

        response = self.client.get(
            reverse('users:division_edit', kwargs={'pk': division.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/division_form.html')
