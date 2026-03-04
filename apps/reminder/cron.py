from django.core.mail import send_mail
from django.conf import settings

def send_network_reminder():
    """
    Fungsi ini akan dipanggil oleh cron job setiap Senin jam 09:00
    """
    # Implementasi sederhana - bisa dikembangkan untuk kirim email atau notifikasi
    print("Reminder: Jangan lupa cek jaringan internet hari ini!")
    # Uncomment untuk kirim email
    # send_mail(
    #     'Reminder: Cek Jaringan',
    #     'Jangan lupa cek jaringan internet hari ini!',
    #     settings.DEFAULT_FROM_EMAIL,
    #     ['admin@company.com'],
    # )
