from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.users.models import Division, UserProfile

from .models import (
    ATKCategory,
    ATKDivisionStock,
    ATKItem,
    ATKRequest,
    ATKRequestLine,
)


class ATKDivisionStockDisplayTests(TestCase):
    def setUp(self):
        self.division = Division.objects.create(name='IT Test')
        self.user = User.objects.create_user(
            username='atk-division-user',
            password='test-password',
        )
        UserProfile.objects.update_or_create(
            user=self.user,
            defaults={'division': self.division},
        )
        category = ATKCategory.objects.create(name='Alat Tulis Test')
        self.item = ATKItem.objects.create(
            name='Pulpen Test',
            category=category,
            current_stock=100,
            minimum_stock=0,
            unit='pcs',
        )
        ATKDivisionStock.objects.create(
            item=self.item,
            division=self.division,
            current_stock=20,
            minimum_stock=0,
        )

    def test_division_stock_table_does_not_show_global_stock_chip(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('atk:item_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<small>IT Test</small>', html=True)
        self.assertNotContains(response, '<small>Global</small>', html=True)
        self.assertNotContains(
            response,
            'Stok yang ditampilkan hanya untuk divisi',
        )
        self.assertNotContains(response, 'atk-mini-chart')


class ATKStockTransferTests(TestCase):
    def setUp(self):
        self.pool_division, _ = Division.objects.get_or_create(name='Administrator')
        self.target_division, _ = Division.objects.get_or_create(name='IT')
        self.admin = User.objects.create_user(
            username='stock-admin',
            password='test-password',
            is_staff=True,
        )
        self.requester = User.objects.create_user(
            username='stock-requester',
            password='test-password',
        )
        UserProfile.objects.update_or_create(
            user=self.requester,
            defaults={'division': self.target_division},
        )
        category = ATKCategory.objects.create(name='Transfer Test')
        self.item = ATKItem.objects.create(
            name='Pulpen Transfer',
            category=category,
            unit='pcs',
        )
        ATKDivisionStock.objects.create(
            item=self.item,
            division=self.pool_division,
            current_stock=100,
        )
        self.atk_request = ATKRequest.objects.create(
            requester=self.requester,
            purpose='Kebutuhan divisi',
        )
        ATKRequestLine.objects.create(
            request=self.atk_request,
            item=self.item,
            quantity=20,
        )

    def test_approval_moves_stock_from_administrator_to_target_division(self):
        self.client.force_login(self.admin)
        self.assertFalse(
            ATKDivisionStock.objects.filter(
                item=self.item,
                division=self.target_division,
            ).exists()
        )

        response = self.client.post(
            reverse('atk:request_review', kwargs={'pk': self.atk_request.pk}),
            {'action': 'approved', 'admin_notes': ''},
        )

        self.assertRedirects(
            response,
            reverse('atk:request_detail', kwargs={'pk': self.atk_request.pk}),
        )
        pool_stock = ATKDivisionStock.objects.get(
            item=self.item,
            division=self.pool_division,
        )
        target_stock = ATKDivisionStock.objects.get(
            item=self.item,
            division=self.target_division,
        )
        self.item.refresh_from_db()
        self.assertEqual(pool_stock.current_stock, 80)
        self.assertEqual(target_stock.current_stock, 20)
        self.assertEqual(self.item.current_stock, 100)

    def test_division_only_sees_items_allocated_to_it(self):
        other_item = ATKItem.objects.create(
            name='Kertas A3',
            category=self.item.category,
            unit='rim',
        )
        ATKDivisionStock.objects.create(
            item=other_item,
            division=self.pool_division,
            current_stock=10,
        )
        ATKDivisionStock.objects.create(
            item=self.item,
            division=self.target_division,
            current_stock=20,
        )
        self.client.force_login(self.requester)

        response = self.client.get(reverse('atk:item_list'))

        self.assertContains(response, self.item.name)
        self.assertNotContains(response, other_item.name)
        self.assertEqual(
            response.context['division_stock_cards'][0]['item_count'],
            1,
        )

    def test_item_form_only_manages_administrator_stock(self):
        other_division = Division.objects.create(name='Purchasing Test')
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse('atk:item_edit', kwargs={'pk': self.item.pk})
        )

        division_names = [
            row['division'].name
            for row in response.context['form'].division_stock_fields
        ]
        self.assertEqual(division_names, [self.pool_division.name])
        self.assertNotIn(other_division.name, division_names)

    def test_staff_default_view_uses_administrator_pool_not_global(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse('atk:item_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_division'], self.pool_division)
        self.assertNotContains(response, 'Total seluruh stok divisi')
        self.assertNotContains(response, '<small>Global</small>', html=True)

    def test_item_detail_renders_stock_and_request_history(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse('atk:item_detail', kwargs={'pk': self.item.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atk/item_detail.html')
        self.assertContains(response, self.item.name)
        self.assertContains(response, self.pool_division.name)
        self.assertContains(response, self.requester.username)
