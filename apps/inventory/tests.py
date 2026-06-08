from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Equipment, EquipmentCategory

class EquipmentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', password='admin123')
        self.user = User.objects.create_user(username='user', password='user123')
        self.category = EquipmentCategory.objects.create(name='Laptop')
        
    def test_equipment_creation_by_admin(self):
        """Test that admin can create equipment"""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('inventory:equipment_add'), {
            'name': 'Test Laptop',
            'inventory_code': 'LAP001',
            'category': self.category.id,
            'status': 'available',
        })
        self.assertEqual(Equipment.objects.count(), 1)
        
    def test_equipment_creation_denied_for_regular_user(self):
        """Test that regular users cannot create equipment"""
        self.client.login(username='user', password='user123')
        response = self.client.post(reverse('inventory:equipment_add'), {
            'name': 'Test Laptop',
            'inventory_code': 'LAP001',
            'category': 'laptop',
            'status': 'available',
        })
        # Should redirect or return 403
        self.assertNotEqual(response.status_code, 200)
