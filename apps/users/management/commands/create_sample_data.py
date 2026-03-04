from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.users.models import EmployeeEmail
from apps.inventory.models import Equipment
from apps.tickets.models import Ticket
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create sample users
        if not User.objects.filter(username='user1').exists():
            user1 = User.objects.create_user('user1', 'user1@company.com', 'password123')
            EmployeeEmail.objects.create(
                user=user1,
                full_name='John Doe',
                employee_id='EMP001',
                primary_email='john.doe@company.com',
                email_password='encrypted_password',
                recovery_email='john.personal@gmail.com',
                recovery_phone='081234567890'
            )
            self.stdout.write(self.style.SUCCESS('Created user: user1'))
        
        # Create sample equipment
        if not Equipment.objects.filter(inventory_code='LAP001').exists():
            Equipment.objects.create(
                name='Dell Latitude 5420',
                inventory_code='LAP001',
                category='laptop',
                specifications='Intel i5, 16GB RAM, 512GB SSD',
                status='available',
                purchase_date=date.today() - timedelta(days=365),
                warranty_until=date.today() + timedelta(days=365)
            )
            self.stdout.write(self.style.SUCCESS('Created equipment: LAP001'))
        
        # Create sample ticket
        user = User.objects.first()
        if user and not Ticket.objects.filter(title='Test Ticket').exists():
            Ticket.objects.create(
                title='Test Ticket',
                reporter=user,
                description='This is a test ticket for demonstration',
                priority='medium',
                status='new'
            )
            self.stdout.write(self.style.SUCCESS('Created sample ticket'))
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
