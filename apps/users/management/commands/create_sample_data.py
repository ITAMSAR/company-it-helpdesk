from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.users.models import EmployeeEmail
from apps.inventory.models import Equipment, EquipmentCategory
from apps.tickets.models import Ticket
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create sample employee emails
        if not EmployeeEmail.objects.filter(employee_id='EMP001').exists():
            EmployeeEmail.objects.create(
                full_name='John Doe',
                employee_id='EMP001',
                primary_email='john.doe@company.com',
                email_password='encrypted_password',
                recovery_email='john.personal@gmail.com',
                recovery_phone='081234567890'
            )
            self.stdout.write(self.style.SUCCESS('Created employee email: EMP001'))
        
        if not EmployeeEmail.objects.filter(employee_id='EMP002').exists():
            EmployeeEmail.objects.create(
                full_name='Jane Smith',
                employee_id='EMP002',
                primary_email='jane.smith@company.com',
                email_password='encrypted_password',
                recovery_email='jane.personal@gmail.com',
                recovery_phone='081234567891'
            )
            self.stdout.write(self.style.SUCCESS('Created employee email: EMP002'))
        
        if not EmployeeEmail.objects.filter(employee_id='EMP003').exists():
            EmployeeEmail.objects.create(
                full_name='Bob Johnson',
                employee_id='EMP003',
                primary_email='bob.johnson@company.com',
                email_password='encrypted_password',
                recovery_email='bob.personal@gmail.com',
                recovery_phone='081234567892',
                is_active=False
            )
            self.stdout.write(self.style.SUCCESS('Created employee email: EMP003'))
        
        # Create sample categories if they don't exist
        elektronik_cat, created = EquipmentCategory.objects.get_or_create(
            name='Elektronik',
            defaults={'description': 'Peralatan elektronik dan teknologi'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created category: Elektronik'))
        
        komputer_cat, created = EquipmentCategory.objects.get_or_create(
            name='Komputer',
            parent=elektronik_cat,
            defaults={'description': 'Desktop, laptop, dan workstation'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created category: Komputer'))
        
        # Create sample equipment
        if not Equipment.objects.filter(inventory_code='LAP001').exists():
            Equipment.objects.create(
                name='Dell Latitude 5420',
                inventory_code='LAP001',
                category=komputer_cat,
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
