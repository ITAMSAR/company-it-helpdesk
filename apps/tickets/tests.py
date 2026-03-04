from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Ticket

class TicketTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin = User.objects.create_superuser(username='admin', password='admin123')
        
    def test_ticket_creation(self):
        """Test creating a ticket"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('tickets:ticket_create'), {
            'title': 'Test Ticket',
            'description': 'Test description',
            'priority': 'medium',
        })
        self.assertEqual(Ticket.objects.count(), 1)
        
    def test_user_can_only_see_own_tickets(self):
        """Test that users can only see their own tickets"""
        other_user = User.objects.create_user(username='other', password='pass123')
        Ticket.objects.create(
            title='Other User Ticket',
            reporter=other_user,
            description='Test',
            priority='low'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tickets:ticket_list'))
        self.assertEqual(len(response.context['tickets']), 0)
        
    def test_admin_can_see_all_tickets(self):
        """Test that admin can see all tickets"""
        Ticket.objects.create(
            title='User Ticket',
            reporter=self.user,
            description='Test',
            priority='low'
        )
        
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('tickets:ticket_list'))
        self.assertEqual(len(response.context['tickets']), 1)
